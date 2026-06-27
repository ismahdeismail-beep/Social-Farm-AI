"""
Calendar Generator Service

Generates content calendars for scheduling.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from enum import Enum
import logging
import uuid

logger = logging.getLogger(__name)


@dataclass
class CalendarEntry:
    """Single calendar entry."""
    id: str
    title: str
    content_type: str
    platform: str
    scheduled_date: datetime
    scheduled_time: str
    topic: str
    hook: str
    caption: str
    hashtags: List[str]
    status: str
    priority: int


class CalendarGenerator:
    """
    Generates content calendars.
    
    Responsibilities:
    - Create daily/weekly/monthly calendars
    - Schedule optimal posting times
    - Balance content types
    - Ensure platform coverage
    """
    
    def __init__(self):
        self.calendars: Dict[str, List[CalendarEntry]] = {}
        self._initialized = False
    
    async def initialize(self):
        """Initialize the calendar generator."""
        if self._initialized:
            return
        
        self._initialized = True
        logger.info("Calendar Generator initialized")
    
    async def generate_calendar(
        self,
        strategy_id: str,
        start_date: datetime,
        end_date: datetime,
        platforms: List[str],
        content_mix: Dict[str, float],
        themes: List[Dict[str, Any]]
    ) -> List[CalendarEntry]:
        """
        Generate a content calendar.
        """
        logger.info(f"Generating calendar for {start_date} to {end_date}")
        
        entries = []
        current_date = start_date
        
        while current_date <= end_date:
            # Generate entries for each day
            daily_entries = await self._generate_daily_entries(
                current_date,
                platforms,
                content_mix,
                themes
            )
            entries.extend(daily_entries)
            current_date += timedelta(days=1)
        
        # Store calendar
        calendar_id = str(uuid.uuid4())
        self.calendars[calendar_id] = entries
        
        logger.info(f"Calendar generated with {len(entries)} entries")
        
        return entries
    
    async def _generate_daily_entries(
        self,
        date: datetime,
        platforms: List[str],
        content_mix: Dict[str, float],
        themes: List[Dict[str, Any]]
    ) -> List[CalendarEntry]:
        """Generate entries for a single day."""
        entries = []
        
        # Determine posting schedule based on day of week
        day_of_week = date.strftime("%A").lower()
        
        posting_schedule = {
            "monday": [("09:00", "linkedin"), ("12:00", "instagram"), ("18:00", "tiktok")],
            "tuesday": [("08:00", "linkedin"), ("17:00", "instagram"), ("20:00", "youtube")],
            "wednesday": [("12:00", "instagram"), ("18:00", "tiktok"), ("19:00", "instagram")],
            "thursday": [("09:00", "linkedin"), ("12:00", "instagram"), ("18:00", "tiktok")],
            "friday": [("08:00", "linkedin"), ("15:00", "instagram"), ("19:00", "tiktok")],
            "saturday": [("10:00", "instagram"), ("14:00", "youtube"), ("20:00", "tiktok")],
            "sunday": [("11:00", "instagram"), ("16:00", "youtube")]
        }
        
        schedule = posting_schedule.get(day_of_week, [])
        
        for time, platform in schedule:
            if platform in platforms:
                # Select theme
                theme = themes[0] if themes else {"name": "General", "keywords": []}
                
                entry = CalendarEntry(
                    id=str(uuid.uuid4()),
                    title=f"{theme['name']} - {platform.title()}",
                    content_type=self._select_content_type(content_mix),
                    platform=platform,
                    scheduled_date=date,
                    scheduled_time=time,
                    topic=theme.get("name", "General"),
                    hook=self._generate_hook(theme),
                    caption=self._generate_caption(theme),
                    hashtags=self._generate_hashtags(theme),
                    status="planned",
                    priority=1
                )
                entries.append(entry)
        
        return entries
    
    def _select_content_type(self, content_mix: Dict[str, float]) -> str:
        """Select content type based on mix."""
        # Simple weighted random selection
        total = sum(content_mix.values())
        r = 50  # Simplified
        
        cumulative = 0
        for content_type, percentage in content_mix.items():
            cumulative += percentage
            if r <= cumulative:
                return content_type
        
        return list(content_mix.keys())[0]
    
    def _generate_hook(self, theme: Dict[str, Any]) -> str:
        """Generate engaging hook."""
        hooks = [
            "Did you know?",
            "Here's the truth about",
            "Stop scrolling! This is important",
            "You won't believe what happens next",
            "The secret to success is"
        ]
        return f"{hooks[0]} {theme.get('name', 'this topic')}"
    
    def _generate_caption(self, theme: Dict[str, Any]) -> str:
        """Generate caption."""
        return f"Discover more about {theme.get('name', 'our content')}. Link in bio!"
    
    def _generate_hashtags(self, theme: Dict[str, Any]) -> List[str]:
        """Generate hashtags."""
        base_hashtags = ["#content", "#socialmedia", "#marketing"]
        theme_hashtags = [f"#{tag}" for tag in theme.get("keywords", [])[:3]]
        return base_hashtags + theme_hashtags
    
    def get_calendar(self, calendar_id: str) -> Optional[List[CalendarEntry]]:
        """Get a calendar by ID."""
        return self.calendars.get(calendar_id)
    
    def list_calendars(self) -> List[str]:
        """List all calendar IDs."""
        return list(self.calendars.keys())


# Singleton instance
calendar_generator = CalendarGenerator()
