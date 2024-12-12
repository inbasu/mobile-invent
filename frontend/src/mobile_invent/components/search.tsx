import TextField from '@mui/material/TextField';
import { Item } from "../datatypes";
import { useContext, useEffect, useState } from 'react';
import { ActionContext, ItemsContext, ResultContext, ItemContext } from '../context';


const searchFilter = (
        item: Item,
        fields: Array<string>,
        querry: string,
) => {
        for (const attr of item.attrs) {
                if (fields.includes(attr.name) && (attr.values[0].label.toLowerCase().includes(querry.toLowerCase()))) {
                        return true;
                }
        }
        return false;
};

export default function SearchBar() {
        const [action, setAction] = useContext(ActionContext);
        const [items, setItems] = useContext(ItemsContext);
        const [results, setResults] = useContext(ResultContext);
        const [item, setItem] = useContext(ItemContext);

        const [label, setLabel] = useState<string>('');
        const [querry, setQuerry] = useState<string>('');
        const [fields, setFields] = useState<Array<string>>([]);

        useEffect(() => {
                if (action === "takeback") {
                        setLabel("Введите номер оборудования или фамилию пользователя(на английском)")
                        setFields(['INV No', "Serial No", "User"])
                } else if (action === 'giveaway') {
                        setLabel("Введите номер реквеста вида ITREQ-000000 или фамилию пользоватея(на английском)")
                } else {
                        setLabel('')
                }

                setItem(null);

        }, [action])


        useEffect(() => {
                if (querry.length > 3) {
                        setResults(items.filter(item => searchFilter(item, fields, querry)));
                } else {
                        setResults(items);
                }
                setItem(null);
        }, [querry])
        return (
                <TextField id="search-bar"
                        onChange={event => setQuerry(event.target.value)}
                        value={querry}
                        label={label}
                        fullWidth
                        disabled={!label} />
        )
}
