import { Moon } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="flex w-full py-5 px-7 justify-between items-center shadow-box">
      <div className="flex items-center text-3xl">
        <Moon
          className="text-emerald-600"
          style={{ width: "1em", height: "1em" }}
          strokeWidth="3"
        />
        <h1 className="ml-2 font-medium text-3xl text-emerald-600">Birlik</h1>
      </div>
    </nav>
  );
}
