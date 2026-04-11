"""
分布式配置中心
"""
import time
from typing import Dict, Any, Optional, Callable


class ConfigItem:
    """配置项"""

    def __init__(self, key: str, value: Any, version: int = 1):
        self.key = key
        self.value = value
        self.version = version
        self.create_time = int(time.time())
        self.update_time = int(time.time())

    def update(self, value: Any) -> bool:
        """更新配置"""
        self.value = value
        self.version += 1
        self.update_time = int(time.time())
        return True


class ConfigWatcher:
    """配置观察者"""

    def __init__(self, callback: Callable):
        self.callback = callback


class ConfigCenter:
    """
    分布式配置中心

    支持：
    - 配置存储
    - 配置监听
    - 热更新
    - 版本管理
    """

    def __init__(self):
        self.configs: Dict[str, ConfigItem] = {}
        self.watchers: Dict[str, list] = {}

    def set(self, key: str, value: Any) -> bool:
        """
        设置配置

        Args:
            key: 配置键
            value: 配置值

        Returns:
            是否设置成功
        """
        if key in self.configs:
            self.configs[key].update(value)
        else:
            self.configs[key] = ConfigItem(key, value)

        self._notify_watchers(key)
        return True

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值
        """
        if key in self.configs:
            return self.configs[key].value
        return default

    def delete(self, key: str) -> bool:
        """
        删除配置

        Args:
            key: 配置键

        Returns:
            是否删除成功
        """
        if key in self.configs:
            del self.configs[key]
            self._notify_watchers(key)
            return True
        return False

    def watch(self, key: str, watcher: ConfigWatcher):
        """
        监听配置变化

        Args:
            key: 配置键
            watcher: 观察者
        """
        if key not in self.watchers:
            self.watchers[key] = []
        self.watchers[key].append(watcher)

    def unwatch(self, key: str, watcher: ConfigWatcher):
        """取消监听"""
        if key in self.watchers:
            self.watchers[key].remove(watcher)

    def _notify_watchers(self, key: str):
        """通知观察者"""
        if key in self.watchers:
            for watcher in self.watchers[key]:
                try:
                    value = self.configs.get(key)
                    watcher.callback(key, value.value if value else None)
                except Exception as e:
                    print(f"Watcher callback error: {e}")

    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return {k: v.value for k, v in self.configs.items()}

    def reload(self, key: str) -> bool:
        """重新加载配置"""
        if key in self.configs:
            self._notify_watchers(key)
            return True
        return False
