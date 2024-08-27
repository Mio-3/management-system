import { supabase } from './supabase';

export const getUserById = async (employeeId: string) => {
  const { data, error } = await supabase
    .from("employees")
    .select("*")
    .eq("employee_id", employeeId)
    .single();

  if (error || !data) {
    return null;
  }

  return data;

}