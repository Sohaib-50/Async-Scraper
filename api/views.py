from rest_framework.views import APIView
from rest_framework.response import Response
from .celery_tasks import scrape_task
from .serializers import ScrapeSerializer, ScrapeResultSerializer
import json

class ScrapeView(APIView):

    serializer_class = ScrapeSerializer

    def post(self, request, *args, **kwargs):

        # get and validate input
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        scrape_url = serializer.validated_data.get("scrape_url")
        async_mode = serializer.validated_data.get("async_mode", False)

        if async_mode:
            print("Scraping Asynchronously..")
            task = scrape_task.delay(scrape_url)  # .delay() to scrape asynchronously
            return Response({
                "scrape_url": scrape_url,
                "message": "Asynchronous scraping started. Make a GET request to /scrape/<scrape_id> with your given ID to check result status and get result if ready.",
                "scrape_id": task.id,
            })
        
        else:
            print("Scraping Synchronously...")
            scraped_contents = scrape_task(scrape_url)  # synchronous call
            print("Scraping complete")
            print(f"Response: {scraped_contents}")
            return Response({
                "scrape_url": scrape_url, 
                "message": "Synchronous scraping completed successfully",
                "scraped_contents": scraped_contents,
            })
    

    def get(self, request, *args, **kwargs):
        return Response({
            "message": "Usage: send post request with model_input (Any) and optionally async_mode (bool) params.",
    
        })
    

class ScrapeResultView(APIView):
    serializer_class = ScrapeResultSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=kwargs)
        serializer.is_valid(raise_exception=True)
        scrape_id = serializer.validated_data.get("scrape_id")
        task = scrape_task.AsyncResult(scrape_id)
        return Response({
            "scrape_id": scrape_id,
            "scraping_task_status": task.status,
            "scraped_contents": task.result if task.result else "Not available yet!"
        })
