
import React from 'react';

const Footer=()=>{
    const time = new Date().getFullYear();
return(
<>
<footer className="w-100  text-center">
    <p>Copyright © {time}</p>
</footer>

</>
);
}

export default Footer;