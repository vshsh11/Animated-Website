import React, { useState } from 'react';

const Contact =() =>{
    const [data,setdata] = useState({
        fname:"",
        email:"",
        number:"",
        message:"",
    });

    const change=(event) =>{
        const {name,value} = event.target;
       setdata((preval)=>{
           return {...preval,
                 [name] : value,            
        }
       })
    };

    const submit=(e)=>{
        e.preventDefault();
        alert(`My name is ${data.fname}, My email is ${data.email}, and number is ${data.number} and message is ${data.message}`)
    };
    return (
        <>
           <div className="my-5">
               <h1 className="text-center">Contact Us</h1>
           </div>
           <div className="container contact_div">
               <div className="row">
                <div className="col-md-6 col-10 mx-auto">
                    <form  onSubmit={submit}>
                    <div className="mb-3">
  <label for="exampleFormControlInput1" className="form-label">Full name</label>
  <input type="text" className="form-control" value={data.fname} name="fname" onChange={change} id="exampleFormControlInput1" placeholder="Enter your name"/>
</div>
                <div className="mb-3">
  <label for="exampleFormControlInput1" className="form-label">Email</label>
  <input type="email" className="form-control" value={data.email} name="email" onChange={change} id="exampleFormControlInput1" placeholder="Enter your mail"/>
</div>
                <div className="mb-3">
  <label for="exampleFormControlInput1" className="form-label">Phone number</label>
  <input type="number" className="form-control" value={data.number} name="number" onChange={change} id="exampleFormControlInput1" placeholder="enter you number"/>
</div>
<div className="mb-3">
  <label for="exampleFormControlTextarea1" className="form-label">Message</label>
  <textarea className="form-control" value={data.message} name="message" onChange={change} id="exampleFormControlTextarea1" rows="3"></textarea>
</div>
<div class="col-12">
    <button className="btn btn-outline-primary" type="submit">Submit form</button>
  </div>
                    </form>
                </div>   
               </div>
           </div> 
        </>
    )

}

export default Contact;