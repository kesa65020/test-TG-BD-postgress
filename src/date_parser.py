from datetime import datetime, timedelta
from typing import Tuple, Optional
import re
from loguru import logger

RUSSIAN_MONTHS = {
    'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
    'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
    'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
}

class DateParser:
    """Parser for Russian date formats and ranges."""
    
    @staticmethod
    def parse_date(date_str: str) -> Optional[str]:
        """Parse Russian date string to ISO format (YYYY-MM-DD)."""
        date_str = date_str.strip()
        
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            pass
        
        try:
            dt = datetime.strptime(date_str, '%d.%m.%Y')
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            pass
        
        for month_name, month_num in RUSSIAN_MONTHS.items():
            pattern = rf'^(\d{{1,2}})\s+{month_name}\s+(\d{{4}})$'
            match = re.match(pattern, date_str)
            if match:
                day = int(match.group(1))
                year = int(match.group(3))
                try:
                    dt = datetime(year, month_num, day)
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    return None
        
        logger.warning(f"Could not parse date: {date_str}")
        return None
    
    @staticmethod
    def parse_date_range(range_str: str) -> Optional[Tuple[str, str]]:
        """Parse Russian date range to ISO format boundaries."""
        range_str = range_str.strip()
        pattern = r'с\s+(.+?)\s+по\s+(.+?)(?:\s+включительно)?$'
        match = re.match(pattern, range_str)
        
        if not match:
            logger.warning(f"Could not parse date range: {range_str}")
            return None
        
        start_str = match.group(1).strip()
        end_str = match.group(2).strip()
        
        start_iso = DateParser.parse_date(start_str)
        end_iso = DateParser.parse_date(end_str)
        
        if not start_iso or not end_iso:
            return None
        
        end_dt = datetime.strptime(end_iso, '%Y-%m-%d')
        end_plus_one = (end_dt + timedelta(days=1)).strftime('%Y-%m-%d')
        
        return (start_iso, end_plus_one)
