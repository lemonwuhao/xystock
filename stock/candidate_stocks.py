import os
import json
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANDIDATE_STOCKS_FILE = os.path.join(PROJECT_ROOT, 'data', 'cache', 'candidate_stocks.json')


def _ensure_dir_exists(file_path):
    """确保文件目录存在"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)


class CandidateStocksManager:
    """候选股票管理器，用于管理用户关注的股票列表"""
    
    def __init__(self):
        self.file_path = CANDIDATE_STOCKS_FILE
        self.candidate_stocks = self.load_candidate_stocks()
    
    def load_candidate_stocks(self) -> List[Dict[str, Any]]:
        """从本地文件加载候选股票列表"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"加载候选股票列表失败: {e}")
            return []
    
    def save_candidate_stocks(self) -> bool:
        """将候选股票列表保存到本地文件"""
        try:
            _ensure_dir_exists(self.file_path)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.candidate_stocks, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存候选股票列表失败: {e}")
            return False
    
    def add_candidate_stock(self, stock_identity: Dict[str, Any]) -> bool:
        """添加股票到候选列表"""
        # 检查股票是否已在列表中
        for stock in self.candidate_stocks:
            if stock['code'] == stock_identity['code'] and stock['market_name'] == stock_identity['market_name']:
                return False  # 股票已存在，无需重复添加
        
        # 添加股票到列表
        self.candidate_stocks.append(stock_identity)
        return self.save_candidate_stocks()
    
    def remove_candidate_stock(self, stock_code: str, market_name: str) -> bool:
        """从候选列表中移除股票"""
        original_length = len(self.candidate_stocks)
        self.candidate_stocks = [
            stock for stock in self.candidate_stocks 
            if not (stock['code'] == stock_code and stock['market_name'] == market_name)
        ]
        
        if len(self.candidate_stocks) < original_length:
            return self.save_candidate_stocks()
        return False  # 股票不在列表中
    
    def is_candidate_stock(self, stock_code: str, market_name: str) -> bool:
        """检查股票是否在候选列表中"""
        for stock in self.candidate_stocks:
            if stock['code'] == stock_code and stock['market_name'] == market_name:
                return True
        return False
    
    def get_candidate_stocks(self) -> List[Dict[str, Any]]:
        """获取候选列表中的所有股票"""
        return self.candidate_stocks.copy()
    
    def clear_candidate_stocks(self) -> bool:
        """清空候选列表"""
        self.candidate_stocks = []
        return self.save_candidate_stocks()


# 创建全局实例
_candidate_stocks_manager = None


def get_candidate_stocks_manager() -> CandidateStocksManager:
    """获取候选股票管理器的全局实例"""
    global _candidate_stocks_manager
    if _candidate_stocks_manager is None:
        _candidate_stocks_manager = CandidateStocksManager()
    return _candidate_stocks_manager


def add_candidate_stock(stock_identity: Dict[str, Any]) -> bool:
    """添加股票到候选列表的便捷函数"""
    manager = get_candidate_stocks_manager()
    return manager.add_candidate_stock(stock_identity)


def remove_candidate_stock(stock_code: str, market_name: str) -> bool:
    """从候选列表中移除股票的便捷函数"""
    manager = get_candidate_stocks_manager()
    return manager.remove_candidate_stock(stock_code, market_name)


def get_candidate_stocks() -> List[Dict[str, Any]]:
    """获取候选列表中的所有股票的便捷函数"""
    manager = get_candidate_stocks_manager()
    return manager.get_candidate_stocks()


def is_candidate_stock(stock_code: str, market_name: str) -> bool:
    """检查股票是否在候选列表中的便捷函数"""
    manager = get_candidate_stocks_manager()
    return manager.is_candidate_stock(stock_code, market_name)


def clear_candidate_stocks() -> bool:
    """清空候选列表的便捷函数"""
    manager = get_candidate_stocks_manager()
    return manager.clear_candidate_stocks()
