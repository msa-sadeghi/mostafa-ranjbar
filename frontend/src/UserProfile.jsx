import { useState } from "react"

function UserProfile(){
    const [user, setUser] =  useState({
        name : 'sara',
        age: 30,
        email:'sara@gmail.com'
    })
    const changeName = (newName)=>{
        setUser({
            ...user,
            name:newName
        })
    }
    return(
        <div>
            <p>Name: {user.name}</p>
            <p>Age: {user.age}</p>
            <button onClick={()=>changeName('nahid')}>ChangeName</button>
        </div>
    )
}
export default UserProfile