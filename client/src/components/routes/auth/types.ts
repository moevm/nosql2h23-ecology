export interface User {
  _id: {
    $oid: string;
  };
  login: string;
  password: string;
  name: string;
  role: string;
}
