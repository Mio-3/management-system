import bcrypt from 'bcryptjs';
import NextAuth from "next-auth";
import type { NextAuthConfig } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { getUserById } from "@/app/lib/db";
import { JWT } from 'next-auth/jwt';
import { User } from 'next-auth';
import { Session } from 'next-auth';

export async function verifyPassword(inputPassword: string, storedPassword: string) {
  return await bcrypt.compare(inputPassword, storedPassword);
}

export const authOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        employeeId: { label: "従業員ID", type: "text"},
        password: { label: "パスワード", type: "password"},
      },
      async authorize(credentials) {
        const user = await getUserById(credentials?.employeeId as string);
        if (user && await verifyPassword(credentials?.password as string, user.password as string)) {
          return { id: user.id, employeeId: user.employee_id, role: user.role };
        }
        return null;
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }: { token: JWT, user?: User }) {
      if (user) {
        const u = user as User & { employeeId: string, role: string};
        token.employeeId = u.employeeId;
        token.userRole = u.role as "employee" | "manager";
      }
      return token;
    },
    async session({ session, token}: { session: Session, token: JWT }) {
      if (token.employeeId && token.userRole) {
        session.user.employeeId = token.employeeId;
        session.user.role = token.userRole as "employee" | "manager";
      }
      return session;
    },
  },
} satisfies NextAuthConfig;

export const { handlers, auth, signIn, signOut } = NextAuth(authOptions);