import Grid from '@mui/material/Grid2';
import { Item, Values } from '../datatypes';
import { border } from "../page";


const getValue = (item: Item, attrs: Array<Values>) => {
        return item.attrs.filter(attr => attrs.includes(attr.name))
}


const itemTable = (item: Item, setItem: Function) => {
        const fields: Array<string> = [
                "INV No", "Serial No", "User",
                "Инв No и модель", "For user"
        ]
        return (
                <Grid container size={12} pl={1}
                        onClick={() => { setItem(item) }}
                        sx={{ borderBottom: border, '&:hover': { background: '#7CB9FF' } }
                        }>
                        <Grid size={12} ><b>{item.label}</b></Grid>
                        {
                                getValue(item, fields).map(field => {
                                        return (
                                                <>
                                                        <Grid size={4}>{field.name}:</Grid>
                                                        <Grid size={8}>{field.values[0]?.label}</Grid>
                                                </>)
                                })
                        }
                </Grid >
        )
};


export default function ItemList({ items, setParentItem }: { items: Array<Item>, setParentItem: Function }) {
        return (
                <Grid container sx={{ height: "100%" }}>
                        {items.map((item) => itemTable(item, setParentItem))}
                </Grid>
        )
}
