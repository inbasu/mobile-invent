import { createContext, Dispatch, SetStateAction } from "react";
import { Item } from "./datatypes";

export const DataContext = createContext<
  [Array<Item>, Dispatch<SetStateAction<Array<Item>>>]
>([[], () => {}]);

export const ItemsContext = createContext<
  [Array<Item>, Dispatch<SetStateAction<Array<Item>>>]
>([[], () => {}]);

export const ResultContext = createContext<
  [Array<Item>, Dispatch<SetStateAction<Array<Item>>>]
>([[], () => {}]);

export const ItemContext = createContext<
  [Item | null, Dispatch<SetStateAction<Item | null>>]
>([null, () => {}]);

export const ActionContext = createContext<
  [string, Dispatch<SetStateAction<string>>]
>(["", () => {}]);

export const LoadingContext = createContext<
  [boolean, Dispatch<SetStateAction<boolean>>]
>([false, () => {}]);

export const StoresContext = createContext<
  [Array<Item> | null, Dispatch<SetStateAction<Array<Item>>>]
>([null, () => {}]);

export const StoreContext = createContext<
  [Item | null, Dispatch<SetStateAction<Item | null>>]
>([null, () => {}]);
