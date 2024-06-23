import streamlit as st
from db import *
import qrcode
import time
import os
from PIL import Image
import pandas as pd
import numpy as np
import cv2
from pyzbar.pyzbar import decode
timestrf1=time.strftime("%Y%m%d-%H%M%S")
def load_image(img):
     im=Image.open(img)
     return im
qr=qrcode.QRCode(version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,border=14)
st.title("Welcome to QR Code Generation Project")
choice=st.sidebar.selectbox("Menu",['Create','Read','Update','Delete','Decode','About'])
create_table()
if(choice=='Create'):
    st.subheader("Generate QR code")
    col1,col2=st.columns(2)
    with col1:
            pn=st.text_input("Enter the Person name")
            mn=st.text_input("Enter the mobile number",max_chars=10)
            st.write("Mobile number should be 10 digits")
    with col2:
            ad=st.text_input("Enter the Address")
            cn=st.selectbox("Course Name",['Python','Data Science','Django'])
            ed=st.date_input("Enter course date")
    if st.button("ADD"):
         add_record(pn,mn,ad,cn,ed)
         st.write(f"Sucessfully record added {pn}")
    raw_data={'person_name':pn,'mobile_number':mn,'course_name':cn}
    if st.button("Generate QR Code"):
         qr.add_data(raw_data)
         qr.make(fit=True)
         img=qr.make_image(fill_colour='black',back_colour='white')
         img_filename='{}{}.png'.format(pn,timestrf1)
         st.success("QR code generated successfully")
         path_for_images=os.path.join('qrimages',img_filename)
         img.save(path_for_images)
         final_image=load_image(path_for_images) #function called
         st.image(final_image)
elif(choice=='Read'):
    st.subheader("Read")
    qr_data=view_all_records()    #function called
    #st.write(qr_data)
    d1=pd.DataFrame(qr_data,columns=['Person name','Mobile no','Address','Course name','Post Date'])
    with st.expander("View all records"):
         st.write(d1)
    with st.expander("No. of courses"):
         counts=d1['Course name'].value_counts().to_frame()
         st.dataframe(counts)
    with st.expander("Date wise student count"):
         counts=d1['Post Date'].value_counts().to_frame()
         st.dataframe(counts)

elif(choice=='Update'):
    st.subheader("Update")
    qr_data=view_all_records()    #function called
    d1=pd.DataFrame(qr_data,columns=['Person name','Mobile no','Address','Course name','Post Date'])
    with st.expander("View all records"):
         st.write(d1)
    list_of_persons=view_update()
    #st.write(list_of_person)
    persons=[i[0] for i in list_of_persons]
    selected_person=st.selectbox("List of persons",persons)
    r1=get_person(selected_person)
    if r1:
         p=r1[0][0]
         q=r1[0][1]
         r=r1[0][2]
         s=r1[0][4]
         #st.write(p,q,r,s)
    col1,col2=st.columns(2)
    with col1:
            pn=st.text_input("Enter the Person name",p)
            mn=st.text_input("Enter the mobile number",q,max_chars=10)
            st.write("Mobile number should be 10 digits")
    with col2:
            ad=st.text_input("Enter the Address",r)
            cn=st.selectbox("Course Name",['Python','Data Science','Django'])
            ed=st.date_input("Enter course date",s)
    if st.button("Update data"):
         update_data=update(mn,cn,ed,pn)
         st.success(f"Record updated successfully {pn}")
    result =view_all_records()    #function called
    d1=pd.DataFrame(result,columns=['Person name','Mobile no','Address','Course name','Post Date'])
    with st.expander("Updated records"):
         st.write(d1)

elif(choice=='Delete'):
    st.subheader("Delete")
    qr_data=view_all_records()    #function called
    d1=pd.DataFrame(qr_data,columns=['Person name','Mobile no','Address','Course name','Post Date'])
    with st.expander("View all records"):
         st.write(d1)
    list_of_persons=view_update()
    #st.write(list_of_person)
    persons=[i[0] for i in list_of_persons]
    selected_person=st.selectbox("List of persons",persons)
    if st.button("Delete Data"):
         delete(selected_person)
         st.success(f"Data is deleted for {selected_person}")
    result =view_all_records()    #function called
    d1=pd.DataFrame(result,columns=['Person name','Mobile no','Address','Course name','Post Date'])
    with st.expander("After deletion of Record"):
         st.write(d1)

elif(choice=='Decode'):
    st.subheader("Decode QR Code")
    qr_image=st.file_uploader("QR code image",type=['png','jpeg','jpg'])
    if qr_image is not None:
          file_bytes=np.asarray(bytearray(qr_image.read()),dtype=np.uint8)
          opencv_image=cv2.imdecode(file_bytes,1)
          c1,c2=st.columns(2)
          with c1:
               st.image(opencv_image)
          with c2:
               st.info("Decode QR Code")
               det=decode(opencv_image)
               st.write(det)
               for i in det:
                    st.write(i[0])         
         



elif(choice=='About'):
    st.subheader("About") 