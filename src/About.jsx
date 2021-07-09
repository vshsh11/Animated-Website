import React from 'react';
import Common from "./Common";
import web from '../src/img/3.png';
const About =() =>{
return (
 <Common 
 name="Welcome to About page"
 imgsrc={web}
 visit="/contact"
 btname="Contact Us"    
 />
)

}

export default About;