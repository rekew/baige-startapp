import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "react-toastify";
import { Api } from "@/api";
import { useAuth } from "@/store/auth";
import { useNavigate } from "react-router";
import Navbar from "@/components/custom/Navbar";

export default function Authentication() {
  const [activeTab, setActiveTab] = useState<"login" | "register">("login");
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const [firstName, setFirstName] = useState<string>("");
  const [surname, setSurname] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [phoneNumber, setPhoneNumber] = useState<string>("");

  const navigate = useNavigate()

  function onSubmit(option: string) {
    if (option === "register") {
      const user = {
        username: username,
        password: password,
        firstName: firstName,
        surname: surname,
        email: email,
        phoneNumber: phoneNumber,
      };

      Api.register(user)
        .then(() => {
          useAuth((state) => state.login())
          navigate('/home')
          console.log("check")
        })
        .catch((error) => {
          const errorMsg = error.response.data.detail[0].msg;
          toast.error(errorMsg);
        });
    } else {
      const user = {
        username: username,
        password: password,
      };

      Api.login(user)
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }

  return (
    <main className="min-h-screen flex flex-col">
      <Navbar></Navbar>

      <section className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-md bg-white shadow-[1.95px_1.95px_2.6px_rgba(0,0,0,0.15)] rounded-xl p-6 flex flex-col items-center gap-4">
          <ul className="flex gap-2.5">
            <li>
              <Button
                onClick={() => setActiveTab("login")}
                className={`shadow-md ${
                  activeTab === "login"
                    ? "bg-emerald-600 text-white hover:bg-emerald-700"
                    : "bg-white text-emerald-600 border border-emerald-600 hover:bg-emerald-50"
                }`}
              >
                Логин
              </Button>
            </li>
            <li>
              <Button
                onClick={() => setActiveTab("register")}
                className={`shadow-md ${
                  activeTab === "register"
                    ? "bg-emerald-600 text-white hover:bg-emerald-700"
                    : "bg-white text-emerald-600 border border-emerald-600 hover:bg-emerald-50"
                }`}
              >
                Регистрация
              </Button>
            </li>
          </ul>
          <Input
            placeholder="Логин"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <Input
            placeholder="Пароль"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {activeTab === "register" && (
            <>
              <Input
                placeholder="Имя"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
              />
              <Input
                placeholder="Фамилия"
                value={surname}
                onChange={(e) => setSurname(e.target.value)}
              />
              <Input
                placeholder="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <Input
                placeholder="Phone Number"
                type="tel"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
              />
            </>
          )}
          <Button
            onClick={() => onSubmit(activeTab)}
            className="bg-blue-600 text-white border border-blue-600 hover:bg-blue-700"
          >
            Submit
          </Button>
        </div>
      </section>
    </main>
  );
}
