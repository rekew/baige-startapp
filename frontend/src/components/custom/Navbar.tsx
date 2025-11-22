import { Motorbike } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="flex w-full py-5 px-7 justify-between items-center shadow-box">
      <div className="flex items-center text-3xl">
        <Motorbike
          className="text-[#8B7355]"
          style={{ width: "1em", height: "1em" }}
          strokeWidth="3"
        />
        <h1 className="ml-2 font-medium text-3xl text-[#8B7355]">Baige</h1>
      </div>
    </nav>
  );
}
