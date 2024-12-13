type Value = {
  label: string;
};

type Values = {
  name: string;
  values: Array<Value>;
};

type Itreq = {
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
