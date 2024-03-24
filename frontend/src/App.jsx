import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [detectingObjects, setDetectingObjects] = useState(false);
  const [outputImage, setOutputImage] = useState(null);
  const [objectCounts, setObjectCounts] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setImagePreview(null);
    setOutputImage(null);
    setObjectCounts(null); 

    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', selectedFile);
    try {
      setDetectingObjects(true);
      const response = await axios.post('https://object-detector-backend.onrender.com/detect', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      const { image, object_counts } = response.data;
      setObjectCounts(object_counts);
      setOutputImage(`data:image/jpeg;base64,${image}`);
      setDetectingObjects(false);
    } catch (error) {
      console.error('Error:', error);
      setDetectingObjects(false);
    }
  };

  return (
    <div className="h-screen flex flex-col gap-10  items-center bg-main bg-no-repeat">
      <div className = ' w-full h-[3rem] text-center'>
      <h1 className="text-3xl text-white">Object Detection App</h1>
      </div>
      <form onSubmit={handleSubmit} >
        <input type="file" accept="image/*" onChange={handleFileChange} className='text-white'/>
        <button  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" type="submit" disabled={!selectedFile || detectingObjects}>
          Detect Objects
        </button>
      </form>
      {detectingObjects && (
        <p className='text-gray-600 text-4xl text-bold text-center'>
          Detecting objects...
        </p>
      )}
      <div className='flex gap-5'>
      {imagePreview && !detectingObjects && (
        <img  className="rounded mx-auto max-w-md" src={imagePreview} alt="Uploaded"/>
      )}
      {outputImage && !detectingObjects && (
        <img  className="rounded mx-auto max-w-md" src={outputImage} alt="Output"  />
      )}
      </div>
      <div className='flex'>
      {objectCounts && !detectingObjects &&(
        <div className='flex flex-col'>
          <h2 className='text-xl'>Objects Detected Are:</h2>
          <ul className='flex gap-5'>
            {Object.entries(objectCounts).map(([className, count]) => (
              <li className = "text-lg" key={className}>
                <span className='text-red-400'>{className}</span> : <span className='text-gray-600'>{count}</span> 
              </li>
            ))}
          </ul>
        </div>
      )}
      </div>
    </div>
  );
}

export default App;
