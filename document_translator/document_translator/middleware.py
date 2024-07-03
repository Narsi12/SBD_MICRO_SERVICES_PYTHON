import json
import logging
from document_translator.enums import ErrorCode
from rest_framework import status
from django.http import JsonResponse, Http404
from django.db.models import ProtectedError
from rest_framework.exceptions import APIException, ValidationError
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger

logger = logging.getLogger(__name__)


class LogRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log user's IP address
        user_ip = self.get_client_ip(request)
        logger.info(f"User IP: {user_ip}")

        # Log request headers
        headers = {k: v for k, v in request.headers.items()}
        logger.info(f"Headers: {headers}")

        # Log request route and parameters
        logger.info(f"Route: {request.path}")
        logger.info(f"Params: {request.GET}")

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class CustomAPIException(APIException):
    def __init__(self, code: ErrorCode, detail=None, status_code=None):
        self.code = code
        self.status_code = status_code if status_code is not None else self.get_status_code()
        self.detail = detail if detail is not None else self.get_default_detail()
        super().__init__(detail = self.detail, code = self.code )
    
    def get_default_detail(self):
        default_details = {
            ErrorCode.INVALID_INPUT: "The input provided is invalid.",
            ErrorCode.NOT_FOUND: "The requested resource was not found.",
            ErrorCode.SERVER_ERROR: "An internal server error occurred.",
            ErrorCode.UNAUTHORIZED: "Authentication credentials were not provided or are invalid.",
            ErrorCode.FORBIDDEN: "You do not have permission to perform this action.",
        }
        return default_details.get(self.code, "An unknown error occurred.")

    def get_status_code(self):
        status_codes = {
            ErrorCode.INVALID_INPUT: status.HTTP_400_BAD_REQUEST,
            ErrorCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
            ErrorCode.SERVER_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
            ErrorCode.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
            ErrorCode.FORBIDDEN: status.HTTP_403_FORBIDDEN,
            ErrorCode.BAD_REQUEST: status.HTTP_400_BAD_REQUEST
        }
        return status_codes.get(self.code, status.HTTP_400_BAD_REQUEST)

class ExceptionHandlingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        json_string = response.content.decode('utf-8')
        if '404' not in json_string:
            string = json.loads(json_string)
            if 'detail' in string:
                string = string['detail']

        if response.status_code == 404:
            if "Page not found" in str(response.content):
                logger.error(f"Page not found exception")
                response_data = {
                    "status": "Page Not Found",
                    "message": "The requested resource was not found."
                }
                return JsonResponse(response_data, status=response.status_code)
        elif response.status_code == 400:
            response_data = {
                    "status": "BAD_REQUEST",
                    "message": string
                }
            return JsonResponse(response_data, status=response.status_code)
        elif response.status_code == 405:
            response_data = {
                    "status": "METHOD_NOT_ALLOWED",
                    "message": string
                }
            return JsonResponse(response_data, status=response.status_code)
        elif response.status_code == 401:
            response_data = {
                    "status": "UNAUTHORIZED",
                    "message": string
                }
            return JsonResponse(response_data, status=response.status_code)
        return response
        
    def process_exception(self, request, exception):
        logging.error(f"Exception occurred: {exception}")

        if isinstance(exception, ValidationError):
            logger.error(f"Validation error occurred: {exception}")
            errors = {}
            for field, error_list in exception.detail.items():
                errors[field] = [error.message for error in error_list]

            response_data = {
                "status": "validation_error",
                "message": "Validation failed",
                "errors": errors
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if isinstance(exception, ProtectedError):
            response_data = {
                "status": "FORBIDDEN",
                "message": str(exception)
            }
            return JsonResponse(response_data, status=status.HTTP_403_FORBIDDEN)
            

        if isinstance(exception, Http404):
            response_data = {
                "status": "NOT_FOUND",
                "message": "The requested resource was not found."
            }
            return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND)
            
        elif isinstance(exception, ObjectDoesNotExist):
            logger.error(f"not_found exception: {str(exception)}")
            response_data = {
                "status": "NOT_FOUND",
                "message": str(exception) 
            }
            return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND)
        
        elif isinstance(exception, KeyError):
            logger.error("Attribute error exception: %s", str(exception))
            response_data = {
                "status": "attribute_error",
                "message": str(exception)
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        elif isinstance(exception, PermissionDenied):
            logger.error(f"permission_denied exception: {str(exception)}")
            response_data = {
                "status": "permission_denied",
                "message": "You do not have permission to perform this action."
            }
            return JsonResponse(response_data, status=status.HTTP_403_FORBIDDEN)
        
        elif isinstance(exception, (EmptyPage, PageNotAnInteger)):
            response_data = {
                "status": "Page Not Found",
                "message": "Invalid page."
            }
            return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND)
        
        elif isinstance(exception, ValueError):
            logger.error("Value error exception: %s", str(exception))
            response_data = {
                "status": "BAD_REQUEST",
                "message": str(exception)
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        elif isinstance(exception, APIException):
            response_data = {
                "code": exception.status_code,
                "status": exception.code,
                "message": str(exception)
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exception, TypeError):
            response_data = {
                "status": "TypeError",
                "message": str(exception)
            }
            return JsonResponse(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error(f"Unhandled exception: {str(exception)}")
            response_data = {
                "status": "server_error",
                "message": "An error occurred while processing your request. Please try again later."
            }
            return JsonResponse(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)