"use client";

import React, { useState } from "react";
import { set } from "react-hook-form";

type LoginFormProps = {
  onSubmit: (staffId: string, password: string) => void;
};

const LoginPage: React.FC<LoginFormProps> = ({ onSubmit }) => {
  const [staffId, setStaffId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    if (!staffId || !password) {
      setError("従業員IDとパスワードを入力してください。");
      setLoading(false);
      return;
    }

    try {
      await onSubmit(staffId, password);
    } catch (err) {
      setError("ログインに失敗しました。");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">シフト管理アプリ</h2>
          <p className="mt-2 text-center text-sm text-gray-600">従業員IDとパスワードを入力してください</p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="staff-id" className="sr-only">
                従業員ID
              </label>
              <input id="staff-id" name="staffId" type="text" required className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="従業員ID" value={staffId} onChange={(e) => setStaffId(e.target.value)} />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                パスワード
              </label>
              <input id="password" name="password" type="password" autoComplete="current-password" required className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="パスワード" value={password} onChange={(e) => setPassword(e.target.value)} />
            </div>
          </div>

          {error && <div className="text-red-500 text-sm text-center">{error}</div>}

          <div>
            <button type="submit" className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
              ログイン
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;