import { useState } from "react";
import api from "../api/axios";

function Login(){
    const [credentials, setCredentials] = useState({
        username:'msa', password:'root'
    })
    const handleSubmit = async(e)=>{
        e.preventDefault()
        try{
           const {data} = await api.post('/token/', credentials)
           localStorage.setItem('token', data.access)
        }
        catch(e){
            console.log(e)
        }
    }
return(
    <form onSubmit={handleSubmit}>
        <button type="submit">login</button>
    </form>
)
}

export default Login