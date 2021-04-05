Tagging and publishing Docker image:

```bash
sudo docker login
sudo docker tag vocabulary_srv robertradnai/vocabulary_srv:"$(git branch --show-current)"
sudo docker push robertradnai/vocabulary_srv:"$(git branch --show-current)"
```

