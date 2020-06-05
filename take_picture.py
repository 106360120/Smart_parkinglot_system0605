# -- coding:UTF-8 --<code>
import cv2
import time
def make_photo(Save_photo):
    """使用opencv拍照"""
    """默認攝像頭"""
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        print(ret)
        if ret:
            cv2.imshow("capture", frame)
            print("n")
    
            """ q關閉攝像頭並存檔"""
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            if Save_photo == int(10):
                print("f")
                file_name = "licence_plate.jpg"
                cv2.imwrite(file_name, frame)
                break
                
        else:
            break
 
    cap.release()
    cv2.destroyAllWindows()
#if __name__ == '__main__':
    #make_photo(10)


 