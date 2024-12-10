type Value = {
  label: string;
};

type Values = {
  name: string;
  values: Array<Value>;
};

export type Item = {
  id: number;
  label: string;
  attrs: Array<Values>;
  joined: Array<Item>;
  itreq?: Array<Item>;
};
