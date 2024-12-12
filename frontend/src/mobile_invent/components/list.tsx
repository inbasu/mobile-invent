import Grid from '@mui/material/Grid2';
import { Item, Values } from '../datatypes';
import { border } from "../page";
import { useContext } from 'react';
import { ActionContext, ItemContext, ResultContext } from '../context';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';


const getValue = (item: Item, attrs: Array<string>) => {
        return item.attrs.filter(attr => attrs.includes(attr.name))
}


const itemTable = (item: Item, setItem: Function, selected: Item | null, action: string) => {
        const fields: Array<string> = [
                "INV No", "Serial No", "User",
                "Инв No и модель", "For user"
        ]
        return (
                <Grid container size={12} pl={1}
                        onClick={() => { setItem(item) }}
                        sx={{
                                borderBottom: border, '&:hover': { background: '#7CB9FF' }, background: item === selected ? '#CCCCCC' :
                                        ((getValue(item, ['State'])[0]?.values[0]?.label === "Free" &&
                                                getValue(item.joined[0], ['Кто принял'])[0]?.values.length != 1) ||
                                                (!['Free', "Working", "ApprovedToBeSent"].includes(getValue(item, ['State'])[0]?.values[0]?.label))) ? '#FFCDD2' : ''

                        }
                        }>
                        {action !== 'takeback' ?
                                <Grid size={12}>
                                        <b>{item.label}</b>

                                </Grid>
                                :
                                <Grid size={12} ><b>{item.label}</b></Grid>
                        }
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


export default function ItemList() {
        const [item, setItem] = useContext(ItemContext);
        const [results, setResults] = useContext(ResultContext);
        const [action, setAction] = useContext(ActionContext);

        return (
                <Grid container sx={{ maxHeight: "100%" }}>
                        {results.map((i) => itemTable(i, setItem, item, action))}
                </Grid>
        )
}
