import { Item } from "./datatypes";

export function actionFilter(
  items: Array<Item>,
  action: string,
  store: string,
): Array<Item> {
  switch (action) {
    case "takeback":
      return items.filter((item) => {
        return item.attrs.filter((attr) => {
          return (
            (attr.name === "State" && attr.values[0].label === "Working") ||
            (attr.name === "User" && attr.values.length)
          );
        }).length;
      });
    case "giveaway":
      if (store !== "IT") {
        return items.filter((item) => item.itreq?.Key);
      } else {
        return items.filter((item) => {
          return item.attrs.filter((attr) => {
            return (
              (attr.name === "State" && attr.values[0].label !== "Working") ||
              (attr.name === "User" && !attr.values.length)
            );
          }).length;
        });
      }
    case "send":
      return items.filter((item) => {
        return item.attrs.filter((attr) => {
          return (
            attr.name === "State" && attr.values[0].label === "ApprovedToBeSent"
          );
        }).length;
      });
    default:
      return items;
  }
}

export function querryFilter(items: Array<Item>, querry: string): Array<Item> {
  if (querry.length > 3) {
    return items.filter((item) => {
      for (const attr of item.attrs) {
        if (
          ["User", "Serial No", "INV No"].includes(attr.name) &&
          attr.values[0]?.label.toLowerCase().includes(querry.toLowerCase())
        ) {
          return true;
        }
      }
      return false;
    });
  } else {
    return items;
  }
}
