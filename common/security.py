import hashlib
import os
import json

class SecurityManager:
    """安全管理器 - 负责密码验证与哈希存储"""
    
    def __init__(self, storage_path: str = None):
        if storage_path is None:
            # 默认存储在用户目录下
            self.storage_path = os.path.join(os.path.expanduser("~"), ".money_tracker", "security.json")
        else:
            self.storage_path = storage_path
            
        self._ensure_storage()

    def _ensure_storage(self):
        """确保安全配置文件存在"""
        directory = os.path.dirname(self.storage_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        if not os.path.exists(self.storage_path):
            self._save_config({"password_hash": None, "salt": None})

    def _save_config(self, config: dict):
        with open(self.storage_path, 'w') as f:
            json.dump(config, f)

    def _load_config(self) -> dict:
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except:
            return {"password_hash": None, "salt": None}

    def has_password(self) -> bool:
        """检查是否设置了密码"""
        config = self._load_config()
        return config.get("password_hash") is not None

    def set_password(self, password: str):
        """设置新密码 (SHA-256 + Salt)"""
        salt = os.urandom(16).hex()
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        
        self._save_config({
            "password_hash": hashed,
            "salt": salt
        })

    def verify_password(self, password: str) -> bool:
        """验证密码"""
        config = self._load_config()
        stored_hash = config.get("password_hash")
        salt = config.get("salt")
        
        if not stored_hash or not salt:
            return True # 未设置密码视为通过
            
        input_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return input_hash == stored_hash
