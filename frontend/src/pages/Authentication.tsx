import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "react-toastify";
import { Api } from "@/api";
import { useAuth } from "@/store/auth";
import { useNavigate } from "react-router";
import Navbar from "@/components/custom/Navbar";

const cities = [
  "Almaty",
  "Astana",
  "Shymkent",
  "Karaganda",
  "Aktobe",
  "Taraz",
  "Pavlodar",
  "Oskemen",
  "Semey",
  "Kostanay",
  "Kyzylorda",
  "Atyrau",
  "Oral",
  "Petropavl",
  "Turkistan",
];

export default function Authentication() {
  const [activeTab, setActiveTab] = useState<"login" | "register">("login");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const [firstName, setFirstName] = useState<string>("");
  const [lastName, setLastName] = useState<string>("");
  const [phoneNumber, setPhoneNumber] = useState<string>("");
  const [dateOfBirth, setDateOfBirth] = useState<string>("");
  const [city, setCity] = useState<string>("");

  const navigate = useNavigate();

  function onSubmit(option: string) {
    if (option === "register") {
      if (
        !firstName ||
        !lastName ||
        !email ||
        !phoneNumber ||
        !dateOfBirth ||
        !city ||
        !password
      ) {
        toast.error("Пожалуйста, заполните все поля");
        return;
      }

      const user = {
        first_name: firstName,
        last_name: lastName,
        email: email,
        phone_number: phoneNumber,
        date_of_birth: dateOfBirth,
        city: city,
        password: password,
      };

      Api.register(user)
        .then(() => {
          useAuth((state) => state.login());
          navigate("/home");
          toast.success("Регистрация успешна!");
        })
        .catch((error) => {
          let errorMsg = "Ошибка при регистрации";
          if (error.response?.data?.detail) {
            if (Array.isArray(error.response.data.detail)) {
              errorMsg = error.response.data.detail[0]?.msg || errorMsg;
            } else {
              errorMsg = error.response.data.detail;
            }
          }
          toast.error(errorMsg);
        });
    } else {
      if (!email || !password) {
        toast.error("Пожалуйста, заполните все поля");
        return;
      }

      const user = {
        email: email,
        password: password,
      };

      Api.login(user)
        .then((response) => {
          useAuth((state) => state.login());
          navigate("/home");
          toast.success("Вход выполнен успешно!");
        })
        .catch((error) => {
          let errorMsg = "Ошибка при входе";
          if (error.response?.data?.detail) {
            errorMsg = error.response.data.detail;
          }
          toast.error(errorMsg);
        });
    }
  }

  return (
    <main className="min-h-screen flex flex-col">
      <Navbar></Navbar>

      <section className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-md bg-[#F5F0E8] shadow-[1.95px_1.95px_2.6px_rgba(0,0,0,0.15)] rounded-xl p-6 flex flex-col items-center gap-4">
          <ul className="flex gap-2.5">
            <li>
              <Button
                onClick={() => setActiveTab("login")}
                className={`shadow-md ${
                  activeTab === "login"
                    ? "bg-[#8B7355] text-white hover:bg-[#6B5A45]"
                    : "bg-[#F5F0E8] text-[#8B7355] border border-[#8B7355] hover:bg-[#E6E6D3]"
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
                    ? "bg-[#8B7355] text-white hover:bg-[#6B5A45]"
                    : "bg-[#F5F0E8] text-[#8B7355] border border-[#8B7355] hover:bg-[#E6E6D3]"
                }`}
              >
                Регистрация
              </Button>
            </li>
          </ul>
          <Input
            placeholder="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
              />
              <Input
                placeholder="Номер телефона"
                type="tel"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
              />
              <Input
                placeholder="Дата рождения"
                type="date"
                value={dateOfBirth}
                onChange={(e) => setDateOfBirth(e.target.value)}
              />
              <Select value={city} onValueChange={setCity}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Выберите город" />
                </SelectTrigger>
                <SelectContent>
                  {cities.map((cityName) => (
                    <SelectItem key={cityName} value={cityName}>
                      {cityName}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </>
          )}
          <Button
            onClick={() => onSubmit(activeTab)}
            className="bg-[#8B7355] text-white border border-[#8B7355] hover:bg-[#6B5A45]"
          >
            Submit
          </Button>
        </div>
      </section>
    </main>
  );
}
