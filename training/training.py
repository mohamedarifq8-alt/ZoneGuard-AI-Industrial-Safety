# تثبيت مكتبة YOLOv8 (Ultralytics) ومكتبة Roboflow
!pip install ultralytics roboflow -q


!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key=)     # (roboflow)هنا مكان هذا الكود باكمله انسخ الكود الذي تحصل علية من  عملية حفظ البيانات وجلبها من موقع
project = rf.workspace("mohamed-arif").project("zoneguard_production_data")
version = project.version(2)
dataset = version.download("yolov8")


# كود التدريب
from ultralytics import YOLO
import os
import shutil

# تحديد مسار ملف البيانات
yaml_path = os.path.join(dataset.location, 'data.yaml')

# نبدأ التدريب من الأوزان الأساسية النظيفة (وليس من النموذج القديم) لضمان عدم النسيان الكارثي
model = YOLO('yolov8m.pt') 

print("\n[INFO] Starting Production Training...")
results = model.train(
    data=yaml_path,
    epochs=150,          # أقصى عدد للجولات
    patience=25,         # الإيقاف المبكر إذا لم يتحسن النموذج
    imgsz=640,
    batch=16,
    project='ZoneGuard_Production',
    name='ppe_model_v2',
    device=0
)

#كود تجهيز الملفات وتحميلها 
import shutil
from ultralytics import YOLO


best_model_path = '/kaggle/working/ضع هنا رابط المخرجات الخاص بك /best.pt'
onnx_model_path = '/kaggle/working/ضع هنا رابط المخرجات الخاص بك /best.onnx'

# تحميل الأوزان وتحويلها
print("\n[INFO] Loading the trained model and exporting to ONNX...")
final_model = YOLO(best_model_path)
final_model.export(format='onnx')

# النسخ للمجلد الرئيسي
shutil.copy(best_model_path, '/kaggle/working/best_production.pt')
shutil.copy(onnx_model_path, '/kaggle/working/best_production.onnx')

print("\n[SUCCESS] تم التحويل والنسخ بنجاح! تفضل بتحميل الملف من القائمة الجانبية.")