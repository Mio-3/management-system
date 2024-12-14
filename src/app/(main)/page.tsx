import LoginPage from "../components/LoginForm";

type LoginFormProps = {
  onSubmit: (staffId: string, password: string) => Promise<void>;
}

export default function Home() {
  return (
    <div className="font-bold">
      <LoginPage />
    </div>
  )
}