import Test from "./pages/Test/Test.tsx"
import Auth from "./pages/Auth/Auth.tsx"

import { BrowserRouter, Route, Routes } from "react-router-dom"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<div style={{ minHeight: '100%' }}>ROOT</div>} />
        <Route path="/test" element={<Test />} />
        <Route path="/auth" element={<Auth />} />
        <Route path="/space" element={<h1>SPACE</h1>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App
