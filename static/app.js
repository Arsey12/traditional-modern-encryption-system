const help = {
 atbash:"Atbash replaces each letter with its opposite in the alphabet. The same operation decrypts it.",
 substitution:"A fixed monoalphabetic key maps each letter to another letter. The same mapping can be reversed to decrypt.",
 aes:"AES-256-GCM uses a random 256-bit secret key and a 12-byte nonce. Save both values to decrypt the ciphertext.",
 rsa:"RSA-OAEP uses a public key to encrypt and the matching private key to decrypt. Direct RSA encryption is suitable only for short messages.",
 hybrid:"Hybrid encryption protects the message with AES-256-GCM and encrypts the one-time AES key with RSA-OAEP.",
 integrated:"Integration mode applies Atbash or Substitution first, encrypts the transformed text with AES-256-GCM, and uses RSA-OAEP to protect the AES key. Decryption reverses the steps."
};
let method="atbash", lastResult=null;
const $=id=>document.getElementById(id);
document.querySelectorAll(".method").forEach(btn=>btn.addEventListener("click",()=>{
 document.querySelectorAll(".method").forEach(x=>x.classList.remove("active"));
 btn.classList.add("active"); method=btn.dataset.method; $("methodHelp").textContent=help[method];
 $("keyArea").classList.toggle("hidden",!["rsa","hybrid","integrated"].includes(method));
 $("traditionalLayer").classList.toggle("hidden",method!=="integrated");
 $("decryptExtras").innerHTML="";
}));
function showStatus(id,msg,isError=false){$(id).textContent=msg;$(id).style.color=isError?"#b42318":"#64748b";}
function addField(parent,label,id,value=""){
 const wrap=document.createElement("div"), lab=document.createElement("label"), area=document.createElement("textarea");
 lab.textContent=label;area.id=id;area.rows=3;area.value=value;area.placeholder=label;
 wrap.append(lab,area);parent.append(wrap);
}
$("generateKeys").addEventListener("click",async()=>{
 try{const r=await fetch("/api/keys",{method:"POST"});const d=await r.json();
 $("publicKey").value=d.public_key;$("privateKey").value=d.private_key;
 showStatus("encryptStatus","RSA key pair generated. Keep the private key confidential.");
 }catch(e){showStatus("encryptStatus",e.message,true);}
});
$("encryptBtn").addEventListener("click",async()=>{
 showStatus("encryptStatus","Encrypting...");
 const payload={method,text:$("plainText").value,public_key:$("publicKey").value};
 if(method==="integrated") payload.traditional_method=$("traditionalMethod").value;
 try{
  const r=await fetch("/api/encrypt",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
  const d=await r.json();if(!r.ok)throw new Error(d.error||"Encryption failed.");
  lastResult=d.result;$("encryptOutput").classList.remove("hidden");
  $("encryptOutput").textContent=JSON.stringify(d.result,null,2);
  $("cipherText").value=d.result.ciphertext;
  $("decryptExtras").innerHTML="";
  if(method==="aes"){addField($("decryptExtras"),"AES secret key (save this securely)","decKey",d.result.key);addField($("decryptExtras"),"AES nonce","decNonce",d.result.nonce);}
  if(method==="rsa"||method==="hybrid"||method==="integrated") addField($("decryptExtras"),"RSA private key","decPrivate",$("privateKey").value);
  if(method==="hybrid"||method==="integrated") addField($("decryptExtras"),"RSA-encrypted AES key","decEncryptedKey",d.result.encrypted_key);
  if(method==="hybrid"||method==="integrated") addField($("decryptExtras"),"AES nonce","decNonce",d.result.nonce);
  if(method==="integrated") addField($("decryptExtras"),"Traditional method used","decTraditional",d.result.traditional_method);
  showStatus("encryptStatus","Encryption successful · "+d.result.algorithm);
 }catch(e){showStatus("encryptStatus",e.message,true);}
});
$("decryptBtn").addEventListener("click",async()=>{
 showStatus("decryptStatus","Decrypting...");
 const payload={method,ciphertext:$("cipherText").value};
 if(method==="aes"){payload.key=$("decKey")?.value;payload.nonce=$("decNonce")?.value;}
 if(method==="rsa"){payload.private_key=$("decPrivate")?.value||$("privateKey").value;}
 if(method==="hybrid"){payload.private_key=$("decPrivate")?.value||$("privateKey").value;payload.encrypted_key=$("decEncryptedKey")?.value;payload.nonce=$("decNonce")?.value;}
 if(method==="integrated"){payload.private_key=$("decPrivate")?.value||$("privateKey").value;payload.encrypted_key=$("decEncryptedKey")?.value;payload.nonce=$("decNonce")?.value;payload.traditional_method=$("decTraditional")?.value||$("traditionalMethod").value;}
 try{
  const r=await fetch("/api/decrypt",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
  const d=await r.json();if(!r.ok)throw new Error(d.error||"Decryption failed.");
  $("plainOutput").classList.remove("hidden");$("plainOutput").textContent=d.plaintext;
  showStatus("decryptStatus","Decryption successful.");
 }catch(e){showStatus("decryptStatus",e.message,true);}
});
