type Value = {
  label: string;
};

export type Values = {
  name: string;
  values: Array<Value>;
};

export type Itreq = {
  Key: string;
  "inv.": string;
  "For user": string;
  "Issue Loction": string;
};

export type Item = {
  id: number;
  label: string;
  attrs: Array<Values>;
  joined: Array<Item>;
  itreq?: Itreq;
};
