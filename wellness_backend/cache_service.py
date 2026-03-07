from django.core.cache import cache
from django.conf import settings
import hashlib
import json


class CacheService:
    """Сервис для кэширования API запросов"""
    
    @staticmethod
    def get_cache_key(prefix, params):
        """Генерирует ключ кэша на основе параметров"""
        params_str = json.dumps(params, sort_keys=True)
        hash_obj = hashlib.md5(params_str.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"
    
    @staticmethod
    def get_food_search_cache(query):
        """Получает кэшированные результаты поиска еды"""
        cache_key = CacheService.get_cache_key('food_search', {'query': query})
        return cache.get(cache_key)
    
    @staticmethod
    def set_food_search_cache(query, data, timeout=3600):
        """Кэширует результаты поиска еды на 1 час"""
        cache_key = CacheService.get_cache_key('food_search', {'query': query})
        cache.set(cache_key, data, timeout)
    
    @staticmethod
    def get_nutrition_cache(food_id):
        """Получает кэшированную информацию о питательности"""
        cache_key = CacheService.get_cache_key('nutrition', {'food_id': food_id})
        return cache.get(cache_key)
    
    @staticmethod
    def set_nutrition_cache(food_id, data, timeout=86400):
        """Кэширует информацию о питательности на 24 часа"""
        cache_key = CacheService.get_cache_key('nutrition', {'food_id': food_id})
        cache.set(cache_key, data, timeout)