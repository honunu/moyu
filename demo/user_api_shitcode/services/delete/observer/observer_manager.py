"""
删除观察者管理器
"""


class DeleteObserver:
    """删除观察者接口"""

    def on_before_delete(self, context):
        """删除前回调"""
        pass

    def on_after_delete(self, context):
        """删除后回调"""
        pass

    def on_delete_failed(self, context):
        """删除失败回调"""
        pass


class DeleteObserverManager:
    """删除观察者管理器"""

    def __init__(self):
        self.observers = []

    def register(self, observer):
        """注册观察者"""
        self.observers.append(observer)

    def unregister(self, observer):
        """取消注册"""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_before_delete(self, context):
        """通知删除前"""
        for observer in self.observers:
            observer.on_before_delete(context)

    def notify_after_delete(self, context):
        """通知删除后"""
        for observer in self.observers:
            observer.on_after_delete(context)

    def notify_delete_failed(self, context):
        """通知删除失败"""
        for observer in self.observers:
            observer.on_delete_failed(context)


class LoggingObserver(DeleteObserver):
    """日志观察者"""

    def on_before_delete(self, context):
        context.add_log("LoggingObserver: before delete")

    def on_after_delete(self, context):
        context.add_log("LoggingObserver: after delete")

    def on_delete_failed(self, context):
        context.add_log("LoggingObserver: delete failed")


class MetricsObserver(DeleteObserver):
    """指标观察者"""

    def __init__(self):
        self.delete_count = 0

    def on_before_delete(self, context):
        self.delete_count += 1
        context.metadata["metrics_delete_count"] = self.delete_count

    def on_after_delete(self, context):
        context.add_log(f"MetricsObserver: total deletes = {self.delete_count}")


class NotificationObserver(DeleteObserver):
    """通知观察者"""

    def on_after_delete(self, context):
        context.add_log("NotificationObserver: delete notification sent")
