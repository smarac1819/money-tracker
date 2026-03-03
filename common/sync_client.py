
import json
import os
from webdav4.client import Client
from datetime import datetime

class SyncManager:
    """双向数据同步管理器 (支持多人协作)"""
    
    REMOTE_FILE = "MoneyTracker_Ledger.json"

    def __init__(self, db, webdav_options: dict = None):
        """
        db: Database 实例
        webdav_options: {
            "base_url": "...",
            "auth": ("user", "pass")
        }
        """
        self.db = db
        self.client = None
        if webdav_options:
            self.connect(webdav_options)

    def connect(self, options: dict):
        try:
            self.client = Client(
                base_url=options["base_url"],
                auth=options.get("auth")
            )
            # 验证连接
            self.client.exists("/")
            return True
        except Exception as e:
            print(f"WebDAV 连接失败: {e}")
            return False

    def sync(self) -> dict:
        """执行同步: Pull -> Merge -> Push"""
        if not self.client:
            return {"status": "error", "msg": "未连接到 WebDAV"}

        stat = {"pulled": 0, "pushed": 0}

        try:
            # 1. Pull: 获取云端数据
            remote_records = []
            if self.client.exists(self.REMOTE_FILE):
                with self.client.open(self.REMOTE_FILE, mode='r') as f:
                    content = f.read()
                    if content:
                        remote_records = json.loads(content)
            
            # 2. Merge (Cloud -> Local)
            # 简单的逻辑：如果云端有 Local 没有的 ID (或者根据 UUID)，则插入
            # 这里的简单实现假设 ID 不冲突 (实际多人应使用 UUID，这里简化处理逻辑：
            # 对比 (amount, timestamp, source, type) 是否完全一致，不一致则通过
            # 更稳妥是：本地所有记录导出 -> 和云端记录合并去重 -> 覆盖云端 -> 更新本地)
            
            # A. 提取本地所有记录
            local_records = self._get_local_records_as_dict()
            
            # B. 合并逻辑: 使用 (created_at, amount, source) 作为唯一键去重
            # 这样 A 和 B 只有在同一秒记了同金额同来源的账才会冲突，概率极小
            merged_map = {}
            
            # 先放入云端记录
            for r in remote_records:
                key = self._make_key(r)
                merged_map[key] = r
            
            # 再合并本地记录 (本地优先？No，并集优先)
            for r in local_records:
                key = self._make_key(r)
                if key not in merged_map:
                    merged_map[key] = r
                    stat["pushed"] += 1 # 这是一个新记录，需要推送到云端
            
            # 检查哪些是从云端新拉下来的
            initial_local_keys = set([self._make_key(r) for r in local_records])
            final_records = list(merged_map.values())
            
            for r in final_records:
                key = self._make_key(r)
                if key not in initial_local_keys:
                    # 这是 cloud 有但 local 没有的 -> 写入本地 DB
                    self._save_to_local_db(r)
                    stat["pulled"] += 1

            # 3. Push: 将合并后的全量数据回写云端
            # 只有当数据有变化时才上传
            if stat["pushed"] > 0 or stat["pulled"] > 0:
                json_str = json.dumps(final_records, ensure_ascii=False, indent=2)
                with self.client.open(self.REMOTE_FILE, mode='w') as f:
                    f.write(json_str)

            return {"status": "success", "msg": f"同步完成: ↓{stat['pulled']} ↑{stat['pushed']}"}

        except Exception as e:
            return {"status": "error", "msg": str(e)}

    def _get_local_records_as_dict(self):
        """将本地 DB 转换为 list of dict"""
        # 获取所有交易
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT amount, type, source, created_at, module_id FROM transactions")
        rows = cursor.fetchall()
        
        records = []
        for r in rows:
            records.append({
                "amount": r[0],
                "type": r[1],
                "source": r[2],
                "created_at": r[3],
                "module_id": r[4] # 注意：多端 module_id 可能会乱，理想情况也应该同步 modules 表。但在 v2.1 简化版，我们假设模块结构一致。
            })
        return records

    def _save_to_local_db(self, record):
        """将单条记录保存到本地"""
        self.db.add_transaction(
            amount=record["amount"],
            trans_type=record["type"],
            source=record["source"],
            module_id=record.get("module_id", 1)
            # created_at 由 DB 自动生成? 不，应该用原始时间
        )
        # Hack: update created_at manually ensure consistency
        cursor = self.db.conn.cursor()
        # 获取刚插入的 ID
        last_id = cursor.lastrowid
        cursor.execute("UPDATE transactions SET created_at = ? WHERE id = ?", (record["created_at"], last_id))
        self.db.conn.commit()

    def _make_key(self, record):
        """生成去重唯一键"""
        return f"{record['created_at']}_{record['amount']}_{record['source']}"
