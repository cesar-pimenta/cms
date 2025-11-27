#!/bin/bash
set -e

ENVIRONMENT=${1:-development}
BRANCH=${2:-develop}

echo "🚀 Deploying to $ENVIRONMENT (branch: $BRANCH)"

# Load environment variables
if [ -f ".env.$ENVIRONMENT" ]; then
    export $(cat ".env.$ENVIRONMENT" | grep -v '#' | xargs)
else
    echo "❌ .env.$ENVIRONMENT not found"
    exit 1
fi

# Pull latest changes
git fetch origin
git checkout $BRANCH
git pull origin $BRANCH

# Pull Docker images
echo "📦 Pulling Docker images..."
docker-compose pull

# Start services
echo "🐳 Starting services..."
docker-compose up -d

# Run migrations
echo "🔄 Running migrations..."
docker-compose exec -T django python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
docker-compose exec -T django python manage.py collectstatic --noinput

# Run tests
if [ "$ENVIRONMENT" != "production" ]; then
    echo "🧪 Running tests..."
    docker-compose exec -T django python manage.py test --verbosity=2
fi

echo "✅ Deploy to $ENVIRONMENT complete!"
