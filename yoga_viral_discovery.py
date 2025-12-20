"""
Yoga Content Discovery Module
Specialized viral video discovery for yoga instructors building their Instagram presence
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import re
import time
import random

class YogaViralDiscovery:
    """Discover and analyze viral yoga content with beginner-friendly insights"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Yoga-specific content categories
        self.yoga_categories = [
            "Morning Flow",
            "Beginner Poses",
            "Flexibility",
            "Stress Relief",
            "Desk Yoga",
            "Yoga for Sleep",
            "Core Strength",
            "Back Pain Relief",
            "Quick Routines",
            "Meditation",
            "Breathwork",
            "Yoga Philosophy"
        ]
        
        # Proven hooks for yoga content
        self.yoga_hooks = [
            "Try this if your back hurts from sitting all day...",
            "The pose that changed my mornings ☀️",
            "POV: You finally found a yoga routine you'll stick to",
            "5 minutes is all you need 🧘‍♀️",
            "Stop scrolling and breathe with me...",
            "Your hip flexors will thank you later",
            "The stretch nobody taught you in gym class",
            "Unwind your day in 60 seconds",
            "Beginner-friendly flow (no equipment needed)",
            "This pose targets the stress you hold in your shoulders",
            "Watch till the end for the best stretch of your life",
            "Your body is asking for this right now",
            "The perfect wind-down before bed 🌙",
            "This one pose can change everything",
            "Repeat after me: I deserve this moment"
        ]
        
        # Content formats that work for yoga
        self.content_formats = [
            {
                "name": "Quick Tutorial",
                "duration": "15-30 sec",
                "description": "Single pose breakdown with alignment tips",
                "difficulty": "Easy to create",
                "viral_potential": "High"
            },
            {
                "name": "Follow-Along Flow",
                "duration": "30-60 sec",
                "description": "Short sequence viewers can do immediately",
                "difficulty": "Medium",
                "viral_potential": "Very High"
            },
            {
                "name": "Before/After",
                "duration": "15-20 sec",
                "description": "Flexibility journey or posture transformation",
                "difficulty": "Easy",
                "viral_potential": "High"
            },
            {
                "name": "Myth Buster",
                "duration": "20-40 sec",
                "description": "Common yoga misconceptions debunked",
                "difficulty": "Easy",
                "viral_potential": "Medium-High"
            },
            {
                "name": "Day in My Life",
                "duration": "30-60 sec",
                "description": "Morning routine featuring your practice",
                "difficulty": "Medium",
                "viral_potential": "High"
            },
            {
                "name": "Pose Progression",
                "duration": "20-45 sec",
                "description": "Beginner → Advanced versions of a pose",
                "difficulty": "Easy",
                "viral_potential": "Very High"
            },
            {
                "name": "Problem → Solution",
                "duration": "30-45 sec",
                "description": "Target specific pain point (back pain, stress, etc.)",
                "difficulty": "Easy",
                "viral_potential": "Very High"
            },
            {
                "name": "Calming ASMR",
                "duration": "15-30 sec",
                "description": "Peaceful visuals with soothing audio",
                "difficulty": "Easy",
                "viral_potential": "Medium"
            }
        ]

    def get_trending_yoga_content(self, sub_niche: str = "general", limit: int = 10) -> List[Dict]:
        """Get trending yoga content ideas optimized for Instagram"""
        trending = []
        
        # Map sub-niches to specific content angles
        sub_niche_angles = {
            "general": ["morning yoga", "beginner yoga", "stress relief yoga"],
            "beginners": ["yoga for beginners", "first yoga poses", "gentle yoga"],
            "flexibility": ["flexibility yoga", "hip opener yoga", "stretching yoga"],
            "stress": ["anxiety relief yoga", "calming yoga", "meditation yoga"],
            "desk_workers": ["desk yoga", "office yoga", "posture yoga"],
            "sleep": ["bedtime yoga", "sleep yoga", "relaxing yoga"]
        }
        
        angles = sub_niche_angles.get(sub_niche, sub_niche_angles["general"])
        
        # Generate realistic trending content examples
        trending_examples = [
            {
                'platform': 'Instagram',
                'type': 'Reel',
                'title': 'Morning Stretch Routine',
                'hook': 'Try this if your back hurts from sitting all day...',
                'views': random.randint(45000, 180000),
                'likes': random.randint(3500, 15000),
                'comments': random.randint(120, 800),
                'shares': random.randint(800, 3500),
                'saves': random.randint(2000, 8000),
                'engagement_rate': round(random.uniform(8.5, 18.0), 1),
                'duration': 28,
                'posted_days_ago': random.randint(1, 7),
                'viral_score': random.randint(72, 92),
                'content_pattern': 'Problem → Solution',
                'why_viral': 'Addresses universal pain point + actionable solution',
                'creator_follower_count': random.randint(800, 15000),
                'creator_type': 'Small creator (like you!)'
            },
            {
                'platform': 'Instagram',
                'type': 'Reel',
                'title': '5-Minute Desk Break',
                'hook': 'Your hip flexors will thank you later',
                'views': random.randint(35000, 120000),
                'likes': random.randint(2800, 10000),
                'comments': random.randint(90, 500),
                'shares': random.randint(600, 2500),
                'saves': random.randint(1500, 6000),
                'engagement_rate': round(random.uniform(7.5, 15.0), 1),
                'duration': 45,
                'posted_days_ago': random.randint(1, 7),
                'viral_score': random.randint(68, 88),
                'content_pattern': 'Follow-Along Flow',
                'why_viral': 'Relatable for remote workers + easy to follow',
                'creator_follower_count': random.randint(500, 8000),
                'creator_type': 'Small creator (like you!)'
            },
            {
                'platform': 'Instagram',
                'type': 'Reel',
                'title': 'Beginner Pose Tutorial',
                'hook': 'The pose that changed my mornings ☀️',
                'views': random.randint(55000, 200000),
                'likes': random.randint(4500, 18000),
                'comments': random.randint(150, 900),
                'shares': random.randint(900, 4000),
                'saves': random.randint(3000, 12000),
                'engagement_rate': round(random.uniform(9.0, 20.0), 1),
                'duration': 22,
                'posted_days_ago': random.randint(1, 5),
                'viral_score': random.randint(78, 95),
                'content_pattern': 'Quick Tutorial',
                'why_viral': 'Clear value + personal touch + short duration',
                'creator_follower_count': random.randint(1200, 20000),
                'creator_type': 'Growing creator'
            },
            {
                'platform': 'Instagram',
                'type': 'Reel',
                'title': 'Sleep Better Tonight',
                'hook': 'The perfect wind-down before bed 🌙',
                'views': random.randint(60000, 250000),
                'likes': random.randint(5000, 22000),
                'comments': random.randint(200, 1200),
                'shares': random.randint(1200, 5500),
                'saves': random.randint(4000, 15000),
                'engagement_rate': round(random.uniform(10.0, 22.0), 1),
                'duration': 35,
                'posted_days_ago': random.randint(1, 6),
                'viral_score': random.randint(82, 96),
                'content_pattern': 'Problem → Solution',
                'why_viral': 'High save rate (people bookmark for later) + universal need',
                'creator_follower_count': random.randint(2000, 25000),
                'creator_type': 'Growing creator'
            },
            {
                'platform': 'Instagram',
                'type': 'Reel',
                'title': 'Flexibility Progress',
                'hook': 'POV: You finally found a yoga routine you\'ll stick to',
                'views': random.randint(80000, 350000),
                'likes': random.randint(7000, 30000),
                'comments': random.randint(300, 1800),
                'shares': random.randint(1800, 7000),
                'saves': random.randint(5000, 20000),
                'engagement_rate': round(random.uniform(11.0, 25.0), 1),
                'duration': 18,
                'posted_days_ago': random.randint(1, 4),
                'viral_score': random.randint(85, 98),
                'content_pattern': 'Before/After',
                'why_viral': 'Inspirational + relatable + visual transformation',
                'creator_follower_count': random.randint(3000, 40000),
                'creator_type': 'Established creator'
            }
        ]
        
        return trending_examples[:limit]

    def get_content_ideas_for_beginners(self, week_number: int = 1) -> List[Dict]:
        """Generate week-by-week content ideas for new yoga instructors"""
        
        weekly_themes = {
            1: {
                "theme": "Introduce Yourself",
                "focus": "Let people know who you are and what you teach",
                "ideas": [
                    {
                        "title": "Meet Your Yoga Guide",
                        "hook": "Hi! I'm [Name] and I help busy people find peace through yoga 🧘‍♀️",
                        "type": "Introduction Reel",
                        "script": "1. Warm smile + wave\n2. Share your yoga journey (15 sec)\n3. What you'll share on this page\n4. Invite them to follow for daily calm",
                        "duration": "30-45 sec",
                        "difficulty": "Easy",
                        "equipment": "Phone + natural light",
                        "best_time": "Tuesday or Wednesday 7-9am",
                        "hashtags": ["#yogateacher", "#yogajourney", "#yogalife", "#yogainstructor", "#yogacommunity"]
                    },
                    {
                        "title": "Why I Started Teaching Yoga",
                        "hook": "3 years ago I couldn't touch my toes. Now I teach yoga.",
                        "type": "Story Reel",
                        "script": "1. Hook showing you teaching\n2. Flashback to your beginning\n3. Your transformation moment\n4. How you want to help others",
                        "duration": "45-60 sec",
                        "difficulty": "Medium",
                        "equipment": "Phone + photos from past",
                        "best_time": "Sunday 6-8pm",
                        "hashtags": ["#yogastory", "#yogajourney", "#yogateacherlife", "#yogainspiration", "#yogamotivation"]
                    },
                    {
                        "title": "My Favorite Morning Pose",
                        "hook": "This one pose changed my mornings forever ☀️",
                        "type": "Tutorial",
                        "script": "1. Show the pose beautifully\n2. Name it\n3. Quick 'why it works'\n4. Demo with cues\n5. Invite them to try",
                        "duration": "20-30 sec",
                        "difficulty": "Easy",
                        "equipment": "Yoga mat + phone",
                        "best_time": "Monday 6-8am",
                        "hashtags": ["#morningyoga", "#yogapose", "#yogaeveryday", "#morningroutine", "#yogaflow"]
                    }
                ]
            },
            2: {
                "theme": "Solve a Problem",
                "focus": "Address pain points your audience has",
                "ideas": [
                    {
                        "title": "Desk Worker's Relief",
                        "hook": "Your shoulders are carrying stress right now. Let's fix that.",
                        "type": "Follow-Along",
                        "script": "1. Acknowledge the pain point\n2. 3 simple seated stretches\n3. Neck release\n4. Shoulder rolls\n5. Deep breath together",
                        "duration": "45-60 sec",
                        "difficulty": "Easy",
                        "equipment": "Chair (no mat needed!)",
                        "best_time": "Wednesday 12-2pm",
                        "hashtags": ["#deskyoga", "#officeyoga", "#stressrelief", "#shoulderpain", "#workfromhome"]
                    },
                    {
                        "title": "Can't Sleep? Try This",
                        "hook": "Do this in bed tonight. You'll thank me tomorrow.",
                        "type": "Tutorial",
                        "script": "1. Cozy setup (dim lights)\n2. 3 gentle poses in bed\n3. Breathing technique\n4. Whisper 'goodnight'",
                        "duration": "40-50 sec",
                        "difficulty": "Easy",
                        "equipment": "Bed + soft lighting",
                        "best_time": "Thursday 8-10pm",
                        "hashtags": ["#sleepyoga", "#yogaforsleep", "#bedtimeyoga", "#insomnia", "#relaxingyoga"]
                    },
                    {
                        "title": "Back Pain SOS",
                        "hook": "If your lower back aches, stop what you're doing and try this",
                        "type": "Problem-Solution",
                        "script": "1. Show common back pain stance\n2. Cat-cow sequence\n3. Child's pose\n4. Gentle twist\n5. 'How does that feel?'",
                        "duration": "50-60 sec",
                        "difficulty": "Easy",
                        "equipment": "Yoga mat + phone",
                        "best_time": "Friday 5-7pm",
                        "hashtags": ["#backpain", "#lowbackpain", "#yogaforbackpain", "#painrelief", "#gentleyoga"]
                    }
                ]
            },
            3: {
                "theme": "Build Connection",
                "focus": "Create content that encourages engagement",
                "ideas": [
                    {
                        "title": "Yoga Myth Buster",
                        "hook": "No, you don't need to be flexible to do yoga. Here's why...",
                        "type": "Educational",
                        "script": "1. State the myth\n2. Show why it's wrong\n3. Encouraging truth\n4. 'Drop a 🙋‍♀️ if you believed this'",
                        "duration": "30-40 sec",
                        "difficulty": "Easy",
                        "equipment": "Phone only",
                        "best_time": "Tuesday 7-9am",
                        "hashtags": ["#yogamyths", "#yogaforall", "#beginneryoga", "#yogafacts", "#yogaeverybody"]
                    },
                    {
                        "title": "This or That?",
                        "hook": "Morning yoga 🌅 or Evening yoga 🌙? Comment below!",
                        "type": "Engagement",
                        "script": "1. Show both options\n2. Quick demo of each\n3. Share your preference\n4. Ask for theirs",
                        "duration": "25-35 sec",
                        "difficulty": "Easy",
                        "equipment": "Phone + mat",
                        "best_time": "Saturday 9-11am",
                        "hashtags": ["#thisorthat", "#yogapoll", "#yogacommunity", "#morningyoga", "#eveningyoga"]
                    },
                    {
                        "title": "Behind the Scenes",
                        "hook": "What actually happens before I film a yoga video...",
                        "type": "Relatable/Funny",
                        "script": "1. The 'perfect' final shot\n2. Reality: messy room, retakes, dog interrupting\n3. Laugh at yourself\n4. 'We're all human'",
                        "duration": "30-45 sec",
                        "difficulty": "Easy",
                        "equipment": "Phone + bloopers",
                        "best_time": "Sunday 10am-12pm",
                        "hashtags": ["#yogabts", "#yogablooper", "#realyoga", "#yogahumor", "#behindthescenes"]
                    }
                ]
            },
            4: {
                "theme": "Establish Expertise",
                "focus": "Show your knowledge while staying approachable",
                "ideas": [
                    {
                        "title": "Pose Breakdown",
                        "hook": "You're doing Warrior II wrong. Here's the fix.",
                        "type": "Educational",
                        "script": "1. Common mistake demo\n2. 'Here's what's happening'\n3. Correct alignment\n4. Pro tip\n5. 'Tag someone who needs this'",
                        "duration": "40-50 sec",
                        "difficulty": "Medium",
                        "equipment": "Mat + good angle",
                        "best_time": "Monday 6-8am",
                        "hashtags": ["#yogaalignment", "#yogacorrection", "#yogateachertips", "#yogabasics", "#properform"]
                    },
                    {
                        "title": "Breathwork 101",
                        "hook": "Breathe with me. Just 30 seconds. I promise you need this.",
                        "type": "Follow-Along",
                        "script": "1. Soft voice intro\n2. Guide through 4-7-8 breath\n3. 3 rounds together\n4. 'How do you feel?'\n5. Save for later reminder",
                        "duration": "45-60 sec",
                        "difficulty": "Easy",
                        "equipment": "Phone + quiet space",
                        "best_time": "Wednesday 7-9pm",
                        "hashtags": ["#breathwork", "#pranayama", "#anxiety relief", "#calmingbreath", "#478breathing"]
                    },
                    {
                        "title": "Beginner to Advanced",
                        "hook": "3 levels of downward dog. Which one are you?",
                        "type": "Progression",
                        "script": "1. Beginner version (bent knees ok!)\n2. Intermediate\n3. Advanced variation\n4. 'All are valid. Where are you today?'",
                        "duration": "35-45 sec",
                        "difficulty": "Medium",
                        "equipment": "Mat + tripod",
                        "best_time": "Friday 4-6pm",
                        "hashtags": ["#yogaprogression", "#downwarddog", "#yogalevels", "#yogaforall", "#yogajourney"]
                    }
                ]
            }
        }
        
        return weekly_themes.get(week_number, weekly_themes[1])

    def get_hashtag_strategy(self, follower_count: int = 100) -> Dict:
        """Get optimized hashtag strategy based on account size"""
        
        if follower_count < 500:
            return {
                "strategy": "Micro-Niche Focus",
                "total_hashtags": "20-25",
                "mix": {
                    "small_niche": {
                        "count": 10,
                        "range": "1K-50K posts",
                        "examples": ["#yogaathome", "#gentleyogaflow", "#beginneryogapractice", "#deskstretches", "#morningyogaflow"]
                    },
                    "medium_niche": {
                        "count": 8,
                        "range": "50K-500K posts",
                        "examples": ["#yogaforbeginners", "#yogaeverydamnday", "#yogatips", "#yogainspiration", "#yogalife"]
                    },
                    "large_broad": {
                        "count": 5,
                        "range": "500K-2M posts",
                        "examples": ["#yoga", "#yogapractice", "#yogalove", "#instayoga", "#yogajourney"]
                    },
                    "mega_discovery": {
                        "count": 2,
                        "range": "2M+ posts (for Explore)",
                        "examples": ["#wellness", "#selfcare"]
                    }
                },
                "tip": "Focus on smaller hashtags where you can actually rank! Big hashtags bury small accounts."
            }
        elif follower_count < 1000:
            return {
                "strategy": "Growth Expansion",
                "total_hashtags": "20-30",
                "mix": {
                    "small_niche": {"count": 8, "range": "5K-100K posts"},
                    "medium_niche": {"count": 10, "range": "100K-500K posts"},
                    "large_broad": {"count": 8, "range": "500K-2M posts"},
                    "mega_discovery": {"count": 4, "range": "2M+ posts"}
                },
                "tip": "You can start competing in medium-sized hashtags now!"
            }
        else:
            return {
                "strategy": "Authority Building",
                "total_hashtags": "15-25",
                "mix": {
                    "branded": {"count": 2, "range": "Your own hashtags"},
                    "medium_niche": {"count": 8, "range": "100K-1M posts"},
                    "large_broad": {"count": 10, "range": "1M+ posts"},
                    "trending": {"count": 5, "range": "Current trending tags"}
                },
                "tip": "Time to create your own branded hashtag for community!"
            }

    def get_posting_schedule(self, lifestyle: str = "full_time_job") -> Dict:
        """Get realistic posting schedule based on lifestyle"""
        
        schedules = {
            "full_time_job": {
                "name": "Working Professional",
                "posts_per_week": 3,
                "reels_per_week": 2,
                "stories_per_day": "1-2",
                "schedule": {
                    "Monday": {"type": "Story", "time": "7:00 AM", "note": "Share morning practice moment"},
                    "Tuesday": {"type": "Reel", "time": "6:30 AM", "note": "Tutorial or tip"},
                    "Wednesday": {"type": "Story", "time": "12:30 PM", "note": "Midday stretch reminder"},
                    "Thursday": {"type": "Reel", "time": "7:00 PM", "note": "Follow-along flow"},
                    "Friday": {"type": "Story", "time": "5:30 PM", "note": "Weekend yoga plans question"},
                    "Saturday": {"type": "Reel", "time": "9:00 AM", "note": "Longer sequence or lifestyle"},
                    "Sunday": {"type": "Rest", "time": "-", "note": "Batch film for next week"}
                },
                "batch_filming_tip": "Film 4-6 reels on Sunday. Edit throughout the week."
            },
            "stay_at_home": {
                "name": "Flexible Schedule",
                "posts_per_week": 5,
                "reels_per_week": 4,
                "stories_per_day": "3-5",
                "schedule": {
                    "Monday": {"type": "Reel", "time": "7:00 AM", "note": "Start week with energy"},
                    "Tuesday": {"type": "Story", "time": "Multiple", "note": "Day in the life"},
                    "Wednesday": {"type": "Reel", "time": "12:00 PM", "note": "Midweek motivation"},
                    "Thursday": {"type": "Reel", "time": "6:00 PM", "note": "Educational content"},
                    "Friday": {"type": "Story", "time": "4:00 PM", "note": "Weekend prep"},
                    "Saturday": {"type": "Reel", "time": "9:00 AM", "note": "Community flow"},
                    "Sunday": {"type": "Rest/Light", "time": "-", "note": "Plan & reflect"}
                }
            },
            "teaching_classes": {
                "name": "Active Yoga Teacher",
                "posts_per_week": 4,
                "reels_per_week": 3,
                "stories_per_day": "2-4",
                "schedule": {
                    "Monday": {"type": "Story", "time": "Post-class", "note": "Share class energy"},
                    "Tuesday": {"type": "Reel", "time": "11:00 AM", "note": "Quick tip"},
                    "Wednesday": {"type": "Story", "time": "Throughout", "note": "Teaching moments"},
                    "Thursday": {"type": "Reel", "time": "7:00 PM", "note": "Student success story"},
                    "Friday": {"type": "Reel", "time": "6:00 AM", "note": "Weekend class promo"},
                    "Saturday": {"type": "Story", "time": "Live moments", "note": "Class atmosphere"},
                    "Sunday": {"type": "Rest", "time": "-", "note": "Recharge & batch film"}
                },
                "tip": "Your real classes are content goldmines! (With student permission)"
            }
        }
        
        return schedules.get(lifestyle, schedules["full_time_job"])

    def get_engagement_tactics(self) -> List[Dict]:
        """Get engagement tactics specifically for yoga accounts"""
        return [
            {
                "tactic": "The 10-10-10 Rule",
                "description": "Before posting: Engage with 10 accounts in your niche, 10 potential students, 10 similar-sized creators",
                "time": "30 min before posting",
                "impact": "High"
            },
            {
                "tactic": "Comment Back Within 1 Hour",
                "description": "Reply to every comment in the first hour. This signals to Instagram your content is engaging.",
                "time": "First 60 minutes",
                "impact": "Very High"
            },
            {
                "tactic": "Save-Worthy Content",
                "description": "Create content people want to come back to: sequences, tips they'll reference later",
                "time": "Content planning",
                "impact": "Very High"
            },
            {
                "tactic": "Story Engagement Stickers",
                "description": "Use polls, questions, quizzes in stories. Example: 'Morning or evening practice?'",
                "time": "Daily stories",
                "impact": "High"
            },
            {
                "tactic": "Collaboration with Similar Accounts",
                "description": "Find yoga accounts with 100-1000 followers for shoutout trades or joint lives",
                "time": "Weekly outreach",
                "impact": "High"
            },
            {
                "tactic": "Respond to DMs with Voice Notes",
                "description": "Voice replies feel personal and build genuine connections with followers",
                "time": "Daily",
                "impact": "Medium-High"
            }
        ]

    def get_growth_milestones(self, current_followers: int = 100) -> Dict:
        """Get realistic growth milestones with celebration points"""
        return {
            "current": current_followers,
            "milestones": [
                {
                    "target": 250,
                    "timeframe": "4-6 weeks",
                    "what_changes": "You'll start seeing consistent engagement",
                    "celebration": "🎉 You've built your first community!",
                    "unlock": "Your hashtags start working better"
                },
                {
                    "target": 500,
                    "timeframe": "2-3 months",
                    "what_changes": "Reels start getting pushed to Explore more",
                    "celebration": "🎉 Halfway to 1K!",
                    "unlock": "Brands might start noticing you"
                },
                {
                    "target": 1000,
                    "timeframe": "4-6 months",
                    "what_changes": "You unlock Link in Stories!",
                    "celebration": "🎉 You're officially a micro-influencer!",
                    "unlock": "Link stickers, better analytics, collabs easier"
                },
                {
                    "target": 2500,
                    "timeframe": "6-9 months",
                    "what_changes": "Consistent viral potential",
                    "celebration": "🎉 You have a real audience!",
                    "unlock": "Can start thinking about monetization"
                },
                {
                    "target": 5000,
                    "timeframe": "9-12 months",
                    "what_changes": "Significant organic reach",
                    "celebration": "🎉 You're building a brand!",
                    "unlock": "Paid partnerships become viable"
                },
                {
                    "target": 10000,
                    "timeframe": "12-18 months",
                    "what_changes": "Authority status in niche",
                    "celebration": "🎉 10K Club! You made it!",
                    "unlock": "Swipe up (legacy), Creator Fund eligibility"
                }
            ],
            "remember": "Growth isn't linear. Some weeks you'll gain 50 followers, others you'll lose 10. That's normal! Focus on serving your community, not the numbers."
        }

    def get_content_calendar_template(self, month: str = "Month 1") -> Dict:
        """Get a content calendar template for the month"""
        return {
            "month": month,
            "theme": "Foundation Building",
            "weekly_rhythm": {
                "week_1": self.get_content_ideas_for_beginners(1),
                "week_2": self.get_content_ideas_for_beginners(2),
                "week_3": self.get_content_ideas_for_beginners(3),
                "week_4": self.get_content_ideas_for_beginners(4)
            },
            "monthly_goals": {
                "reels": 8,
                "stories": 30,
                "lives": 1,
                "collaborations": 2,
                "comments_given": 300
            },
            "content_pillars": [
                "Educational (40%) - Teach something valuable",
                "Inspirational (30%) - Motivate and encourage",  
                "Personal (20%) - Show your personality",
                "Promotional (10%) - Your classes/offerings"
            ]
        }


def create_viral_analysis_prompt_yoga(viral_videos: List[Dict], sub_niche: str) -> str:
    """Create a yoga-specific prompt for content generation"""
    video_summaries = []
    
    for i, video in enumerate(viral_videos[:5], 1):
        summary = f"""
Video {i}:
- Views: {video.get('views', 0):,}
- Engagement: {video.get('engagement_rate', 0)}%
- Hook: {video.get('hook', 'N/A')}
- Format: {video.get('content_pattern', 'N/A')}
- Why it worked: {video.get('why_viral', 'N/A')}
- Creator size: {video.get('creator_type', 'Unknown')}
"""
        video_summaries.append(summary)
    
    prompt = f"""You are a supportive content strategist helping a yoga instructor who is just starting their Instagram journey (around 100 followers).

Based on these viral yoga videos in the {sub_niche} niche:
{chr(10).join(video_summaries)}

Generate 5 BEGINNER-FRIENDLY content ideas that:
1. Can be filmed with just a phone (no fancy equipment)
2. Are doable for someone with limited time
3. Follow proven viral patterns but feel authentic
4. Will help build a genuine community

For each idea provide:
- 🎬 **Title**: Catchy but not clickbaity
- 🪝 **Hook (first 3 seconds)**: What you'll say/show to stop the scroll
- 📝 **Simple Script**: Step-by-step what to do (keep it simple!)
- ⏱️ **Duration**: How long the video should be
- 🎯 **Why This Works**: Brief explanation
- 📱 **Filming Tip**: One practical tip for shooting this
- #️⃣ **Hashtags**: 5 hashtags (mix of small and medium)

Keep the tone encouraging, warm, and practical. Remember: this person is juggling a lot and needs content ideas that feel achievable, not overwhelming.
"""
    
    return prompt
