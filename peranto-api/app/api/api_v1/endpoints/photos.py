#A necessity for a smooth Identity Check user experience.
#Live Photos are images (i.e. selfies) of the client's face. Typically, along with an ID document, they are used to perform .
#Upon creating a Live Photo, the following inspections are conducted:
#Faces Analysis: checks if a face is detected and that the number of faces does not exceed 1.
#Facial Obstructions: checks if facial features are covered or not visible.
#Facial Orientation: checks if a face is at an optimal position.
#Liveness Check: checks if a photo is genuine and is not a spoofed photo of an image or photo-of-a-photo.
#The live photos API allows you to upload, retrieve, download, and delete live photos. You can retrieve a specific live photo as well as a list of all your client's live photos.


from fastapi import APIRouter, Query
