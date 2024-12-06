type Value = {
  label: Array<string>;
};

type Values = {
  name: string;
  values: Array<Value>;
};

export type Item = {
  id: number;
  label: string;
  attrs: Array<Values>;
  ereq?: Item;
};
