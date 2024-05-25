import cv2
import os
#işletim sistemi için os import ettik. verileri klasörden toplaycağız.
import tensorflow as tf
#pip install tensorflow ile tensorflowu indirdik terminalde
from tensorflow import keras
from PIL import Image
# PIL okumuyordu bu yüzden terminalde 'python3 -m pip install Pillow' yazdım.
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import normalize, to_categorical
#modelimizi oluşturmak için bazı importları yazıyorum
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense


image_directory='C:\\Users\\ekinf\\Desktop\\BITIRMEPROJE\\tumorProje\\my_site\\machine_learning\\datasets\\'
#yolu yarattık
dataset=[]
label=[]
#görüntüyü bağımlı ve bağımsız değişkene dönüştüreceğiz.


no_tumor_images=os.listdir(image_directory+ 'no/')
yes_tumor_images=os.listdir(image_directory+ 'yes/')

#burda bir kere belirledik boyut için bunu yazacağız
INPUT_SIZE=64

#tüm resimler için yeni bir klasör oluşturdum.

#print(no_tumor_images)

#path= 'no1157.jpg'

#print(path.split('.')[1])

#BEYİN TÖMÜRÜ YOK
#resimimizin java resmi olup olmadığını kontrol ediyorum.
# Görselleri okuyorum.
for i , image_name in enumerate(no_tumor_images):
    if(image_name.split('.')[1]=='jpg'):
        image=cv2.imread(image_directory+'no/'+image_name)
        image=Image.fromarray(image, 'RGB')
        #Görüntüyü rgb'ye dönüştürdüm
        #model oluşturma amacıyla yeniden boyutlandırıyorum.
        image=image.resize((INPUT_SIZE, INPUT_SIZE))
        dataset.append(np.array(image))
        label.append(0)

#BEYİN TÖMÜRÜ VAR
for i , image_name in enumerate(yes_tumor_images):
    if(image_name.split('.')[1]=='jpg'):
        image=cv2.imread(image_directory+'yes/'+image_name)
        image=Image.fromarray(image, 'RGB')
        #Görüntüyü rgb'ye dönüştürdüm
        #model oluşturma amacıyla yeniden boyutlandırıyorum.
        image=image.resize((INPUT_SIZE, INPUT_SIZE))
        dataset.append(np.array(image))
        label.append(1)

#veri setini yazdıracağız
#print(len(dataset))
#print(len(label))
#bu ikisini çalıştırdığımızda datasetin ve labelın aynı olduğunu ve çıktı olarak 3000 verdiğini görüyoruz
#bu da demek ki tüm resimlere doğru şekilde erişiyoruz

dataset = np.array(dataset)
label = np.array(label)

#şimdi bu görüntüleri numpy dizisine dönüştürmemiz lazım
#veri tarafını eğitimin %80(0.8)'ine, test için de %20(0.2)'ye bölecek
x_train, x_test, y_train, y_test= train_test_split(dataset,label,test_size=0.2,random_state=0)

#Reshape = (n, image_width, image_height, n_channel)

#print(x_train.shape)
#bu kodu çalıştırdığımda output olarak (2400, 64, 64, 3) aldım. 2440 resimlerin sayısı, 64ler boyut belirtiyor. 64x64. ve 3 de rgb kanallarını belirtiyor.
#print(y_train.shape)
#y de aynı
#erişilen test için yazacağız
#print(x_test.shape)
#print(y_test.shape)
#bu koddan sonra çıktı olarak
# (2400, 64, 64, 3)
# (2400,)
# (600, 64, 64, 3)
# (600,) aldım. bu da dataların %80'e %20 bölündüğünü gösteriyor. toplamları da 3000 ediyor.

x_train = normalize(x_train, axis=1)
x_test = normalize(x_test, axis=1)

y_train = to_categorical(y_train, num_classes=2)
y_test = to_categorical(y_test, num_classes=2)

#Şimdi modelimizi oluşturacağız

model = Sequential()

model.add(Conv2D(32, (3,3), input_shape=(INPUT_SIZE, INPUT_SIZE, 3)))
#aktivasyon fonksiyonunu ekliyorum
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(32, (3,3), kernel_initializer='he_uniform'))
#aktivasyon fonksiyonunu ekliyorum
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64, (3,3), kernel_initializer='he_uniform'))
#aktivasyon fonksiyonunu ekliyorum
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

#tüm görüntüleri tek faktörde yapmamız lazım bu yüzden düzleştireceğiz

model.add(Flatten())
model.add(Dense(64))
# basit bir CNN modeli
model.add(Activation('relu'))
#uyma sorununu en aza indireceğiz
model.add(Dropout(0.5))
#neden dense'i 1 yaptım. çünkü binary class kullanıyorum. çıktılarım evet veya hayır olacak
model.add(Dense(2))
#aktivasyon kodunu cidden kullanan modeli yazacağım
model.add(Activation('softmax'))

# Dense neden 1 yaptık not:
# Binary CrossEntropy=1, sigmoid
# Categorical Entropy= 2, softmax, daha sonradan bunu kullandım

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#kaybı çapraz doğrulama olarak alacak, modelin gerçek dünya verileriyle nasıl performans göstereceği hakkında daha doğru bir fikir edinilir.

#modeli beslyeceğim
model.fit(x_train, y_train, batch_size=16, verbose=1, epochs=10, validation_data=(x_test, y_test), shuffle=False)

#modeli klasörümüze kaydedelim
model.save('BrainTumorModel.h5', save_format='h5')