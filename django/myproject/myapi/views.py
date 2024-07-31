# myapi/views.py
from django.http import JsonResponse
from django.views import View
from myapi import my_script  # Use absolute import
from django.db import connection
import subprocess

class RunScriptView(View):
    def get(self, request, *args, **kwargs):
        result = my_script.execute_task()  # Call the function from your script
        return JsonResponse({'message': result})
   
class RunSQLQueryView(View):
    def get(self, request, *args, **kwargs):
        # Step 1: Run the Python script to fetch/update data
        try:
            # Replace with the actual path to your Python script
            script_path = 'postgress_ingest.py'
            result = subprocess.run(['python', script_path], capture_output=True, text=True)
            script_output = result.stdout if result.returncode == 0 else result.stderr
            
            if result.returncode != 0:
                return JsonResponse({'error': f"Script error: {script_output}"}, status=500)
        except Exception as e:
            return JsonResponse({'error': f"Failed to run script: {str(e)}"}, status=500)

        # Step 2: Execute the SQL query after running the script
        sql_query = request.GET.get('query', 'select * from company_data')  # Default query if not provided

        if not sql_query:
            return JsonResponse({'error': 'No SQL query provided'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, row)) for row in rows]
            
            return JsonResponse(result, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
  
class RunSQLQueryOnly3(View):
    def get(self, request, *args, **kwargs):
        sql_query = request.GET.get('query', 'select * from company_data_test')  # Default query if not provided

        if not sql_query:
            return JsonResponse({'error': 'No SQL query provided'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, row)) for row in rows]
            
            return JsonResponse(result, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

  
class RunSQLQueryView2(View):
    def get(self, request, *args, **kwargs):
        # Step 1: Run the Python script to fetch/update data
        try:
            # Replace with the actual path to your Python script
            script_path = 'ingest_test.py'
            result = subprocess.run(['python', script_path], capture_output=True, text=True)
            script_output = result.stdout if result.returncode == 0 else result.stderr
            
            if result.returncode != 0:
                return JsonResponse({'error': f"Script error: {script_output}"}, status=500)
        except Exception as e:
            return JsonResponse({'error': f"Failed to run script: {str(e)}"}, status=500)

        # Step 2: Execute the SQL query after running the script
        sql_query = request.GET.get('query', 'select * from company_data_test')  # Default query if not provided

        if not sql_query:
            return JsonResponse({'error': 'No SQL query provided'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, row)) for row in rows]
            
            return JsonResponse(result, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
 