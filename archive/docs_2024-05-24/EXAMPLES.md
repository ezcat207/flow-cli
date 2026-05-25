# Flow CLI Examples

Practical examples for common use cases.

## Image Generation

### Basic Image

```bash
flow generate image "a cute cat wearing sunglasses"
```

### High-Quality Photo

```bash
flow generate image "professional portrait photo of a woman, studio lighting" \
  --style photorealistic \
  --ratio 9:16 \
  --negative "blurry, low quality, amateur"
```

### Artistic Style

```bash
flow generate image "abstract geometric patterns in vibrant colors" \
  --style artistic \
  --ratio 1:1
```

### Reproducible Results

```bash
flow generate image "futuristic cityscape" \
  --seed 42 \
  --ratio 16:9
```

## Video Generation

### Simple Video

```bash
flow generate video "waves crashing on a beach at sunset"
```

### Cinematic Shot

```bash
flow generate video "wide establishing shot of a medieval castle on a hill" \
  --duration 8 \
  --camera dolly_in \
  --ratio 21:9
```

### Product Demo

```bash
flow generate video "smartphone rotating on a white background" \
  --camera orbit \
  --duration 5 \
  --ratio 1:1
```

### Animate a Still Image

```bash
# First, generate an image
flow generate image "portrait of a person smiling" \
  --ratio 9:16 \
  --download portrait.png

# Then animate it
flow generate video "person turns head and smiles at camera" \
  --from-image portrait.png \
  --duration 3
```

## Asset Management

### List Recent Videos

```bash
flow list --type video --limit 10
```

### Find Specific Asset

```bash
flow list | grep "mountain landscape"
```

### Download Multiple Assets

```bash
# Get all asset IDs
flow list --output json | jq -r '.assets[].id' > asset_ids.txt

# Download each
while read asset_id; do
  flow download "$asset_id"
done < asset_ids.txt
```

### Clean Up Old Assets

```bash
# List assets older than 30 days
flow list --output json | \
  jq -r '.assets[] | select(.created_at < "2026-04-15") | .id' | \
  while read id; do
    flow delete "$id" --yes
  done
```

## Scripting

### Batch Image Generation

```bash
#!/bin/bash

PROMPTS=(
  "a red sports car"
  "a blue ocean"
  "a green forest"
  "a yellow sunset"
)

for prompt in "${PROMPTS[@]}"; do
  echo "Generating: $prompt"
  flow generate image "$prompt" --output json | jq -r '.asset_id' >> asset_ids.txt
done
```

### Video Compilation Pipeline

```bash
#!/bin/bash

# Generate multiple video clips
flow generate video "scene 1: opening shot of city" --download scene1.mp4
flow generate video "scene 2: close-up of character" --download scene2.mp4
flow generate video "scene 3: final wide shot" --download scene3.mp4

# Combine with ffmpeg
ffmpeg -i scene1.mp4 -i scene2.mp4 -i scene3.mp4 \
  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1[outv]" \
  -map "[outv]" final.mp4
```

### Monitor Generation Queue

```bash
#!/bin/bash

JOB_ID=$1

while true; do
  STATUS=$(flow status "$JOB_ID" --output json | jq -r '.status')
  PROGRESS=$(flow status "$JOB_ID" --output json | jq -r '.progress')

  echo "Status: $STATUS ($PROGRESS%)"

  if [ "$STATUS" = "completed" ]; then
    echo "Generation complete!"
    break
  elif [ "$STATUS" = "failed" ]; then
    echo "Generation failed!"
    exit 1
  fi

  sleep 5
done
```

## Integration with Other Tools

### Use with ImageMagick

```bash
# Generate image
flow generate image "colorful abstract pattern" --download pattern.png

# Apply effects
convert pattern.png -blur 0x8 pattern_blurred.png
convert pattern.png -swirl 180 pattern_swirled.png
```

### Use with FFmpeg

```bash
# Generate video
flow generate video "nature scene" --download nature.mp4

# Add audio
ffmpeg -i nature.mp4 -i music.mp3 -c:v copy -c:a aac nature_with_audio.mp4

# Create GIF
ffmpeg -i nature.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" nature.gif
```

### Use with jq for JSON Processing

```bash
# Get URLs of all completed videos
flow list --type video --output json | \
  jq -r '.assets[] | select(.status == "completed") | .url'

# Count assets by type
flow list --output json | \
  jq -r '.assets | group_by(.type) | map({type: .[0].type, count: length})'

# Get total size of all assets
flow list --output json | \
  jq -r '.assets[].metadata.size_bytes' | \
  awk '{sum+=$1} END {print sum/1024/1024 " MB"}'
```

## Creative Workflows

### Storyboard Generation

```bash
#!/bin/bash

# Generate storyboard frames
flow generate image "scene 1: hero enters room" --ratio 16:9 --download frame1.png
flow generate image "scene 2: hero discovers treasure" --ratio 16:9 --download frame2.png
flow generate image "scene 3: hero battles guardian" --ratio 16:9 --download frame3.png

# Create storyboard
montage frame*.png -tile 3x1 -geometry +10+10 storyboard.png
```

### A/B Testing Visuals

```bash
#!/bin/bash

# Generate variations
flow generate image "product ad" --seed 1 --download variant_a.png
flow generate image "product ad" --seed 2 --download variant_b.png
flow generate image "product ad" --seed 3 --download variant_c.png

# Compare side-by-side
montage variant_*.png -tile 3x1 -geometry +10+10 comparison.png
```

### Social Media Content

```bash
# Instagram post (1:1)
flow generate image "motivational quote on aesthetic background" \
  --ratio 1:1 \
  --download instagram_post.png

# Instagram story (9:16)
flow generate video "behind the scenes of our product" \
  --ratio 9:16 \
  --duration 5 \
  --download instagram_story.mp4

# YouTube thumbnail (16:9)
flow generate image "eye-catching thumbnail with bold text" \
  --ratio 16:9 \
  --download youtube_thumb.png
```

## Automation

### Cron Job for Daily Content

```bash
# Add to crontab: crontab -e
# 0 9 * * * /path/to/daily_content.sh

#!/bin/bash

DATE=$(date +%Y-%m-%d)
PROMPT="daily inspiration for $DATE"

flow generate image "$PROMPT" \
  --ratio 1:1 \
  --download "/var/www/content/daily_$DATE.png"

# Post to social media (use your API)
# curl -X POST ... -F "image=@/var/www/content/daily_$DATE.png"
```

### Webhook Integration

```bash
#!/bin/bash

# Receive webhook
# POST /generate-content
# {"prompt": "...", "type": "image", "webhook_url": "..."}

PROMPT="$1"
TYPE="$2"
WEBHOOK_URL="$3"

JOB_ID=$(flow generate $TYPE "$PROMPT" --no-wait --output json | jq -r '.job_id')

# Poll until complete
while true; do
  STATUS=$(flow status "$JOB_ID" --output json)
  STATE=$(echo "$STATUS" | jq -r '.status')

  if [ "$STATE" = "completed" ]; then
    # Send webhook
    curl -X POST "$WEBHOOK_URL" \
      -H "Content-Type: application/json" \
      -d "$STATUS"
    break
  fi

  sleep 5
done
```

## Tips & Tricks

### Speed Up by Not Waiting

```bash
# Submit multiple jobs in parallel
flow generate video "scene 1" --no-wait &
flow generate video "scene 2" --no-wait &
flow generate video "scene 3" --no-wait &

# Check all later
flow list
```

### Reuse Successful Seeds

```bash
# Generate with random seed
OUTPUT=$(flow generate image "landscape" --output json)
SEED=$(echo "$OUTPUT" | jq -r '.seed')
ASSET_ID=$(echo "$OUTPUT" | jq -r '.asset_id')

# If you like it, reuse the seed for variations
flow generate image "similar landscape but at night" --seed $SEED
```

### Save Prompts for Later

```bash
# Save successful prompts
echo "a serene mountain landscape at sunset" >> prompts.txt
echo "cinematic shot of a futuristic city" >> prompts.txt

# Regenerate later
while read prompt; do
  flow generate image "$prompt"
done < prompts.txt
```
