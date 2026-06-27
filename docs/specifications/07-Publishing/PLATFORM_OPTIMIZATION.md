# PLATFORM_OPTIMIZATION

## Purpose
The Platform Optimization module ensures that content is tailored to the unique technical constraints and engagement best practices of each social platform.

## Optimization Parameters

| Platform | Caption Limit | Media Formats | Aspect Ratios | Hashtag Strategy |
| :--- | :--- | :--- | :--- | :--- |
| TikTok | 2200 | MP4, MOV | 9:16 | 3-5 trending |
| Instagram | 2200 | JPEG, PNG, MP4 | 1:1, 4:5, 9:16 | 15-30 mixed |
| X | 280 | JPEG, GIF, MP4 | 16:9, 1:1 | 1-2 relevant |
| LinkedIn | 3000 | JPEG, PNG, MP4 | 1:1, 16:9 | 3-5 professional |

## Implementation
The `OptimizerService` applies these rules during the content pipeline stage:
1. **Truncation:** If captions exceed limits.
2. **Resizing:** Using `MEDIA_PROCESSING` to force media into accepted aspect ratios.
3. **Hashtag Injection:** Automatically appending platform-specific hashtag sets.
