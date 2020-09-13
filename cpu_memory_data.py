import psutil

"""
README:
A program to extract CPU memory for user input in 
our ws.py REST API web server, after extracting the data we
can send a req (POST or PUT) with the data via Postman.
---------------------------------
ex: 
data extracted and stored in variable
cpu_memory_data = {'client_name': 'Daniel', 'total': '15.86GB',
                    'available': '1.39GB', 'used': '14.47GB',
                    'percentage': 91.2}
cpu_memory_data will be implemented in the postman application 
as raw json format dictionary.
---------------------------------
"""


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


svmem = psutil.virtual_memory()
total = get_size(svmem.total)
available = get_size(svmem.available)
used = get_size(svmem.used)
percentage = svmem.percent
client_name = "Daniel"

cpu_memory_data = {"client_name": client_name, "total": total,
                   "available": available, "used": used,
                   "percentage": percentage}

