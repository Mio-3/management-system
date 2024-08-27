import "next-auth";
import "next-auth/jwt";

declare module "next-auth" {
  interface Session {
    user: {
      employeeId: string;
      role: "employee" | "manager";
    };
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    employeeId?: string;
    userRole?: "employee" | "manager";
  }
}
