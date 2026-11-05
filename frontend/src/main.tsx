import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './main.css'

import { Toaster } from 'sonner';
import { toast } from 'sonner';
import { setAPI } from './orbit-backend-handler/api.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Toaster theme='dark' richColors position='bottom-right' duration={3500} />
    <App />
  </StrictMode>,
)

const api_status = await setAPI();
console.log(api_status)

if (api_status != 0) {
  toast.error("Our backend is facing some issues, please try again later!") 
}