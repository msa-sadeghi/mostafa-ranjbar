import axios from "axios"

function Documents(){
    const data = axios.get('http://127.0.0.1:8000/api/documents/')
    console.log(data)
}

export default Documents