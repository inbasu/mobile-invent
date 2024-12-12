import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { useContext, useEffect } from 'react';
import { ActionContext, DataContext, ItemsContext, ResultContext } from '../context';
import { Item } from '../datatypes';


const search = (items: Array<Item>, action: string) => {
        switch (action) {
                case "takeback":
                        return items.filter((item) => {

                                return item.attrs.filter(attr => {

                                        return ((attr.name == "State" && attr.values[0].label == "Working") ||
                                                (attr.name == "User" && attr.values.length))
                                }).length

                        })
                case "giveaway":
                        return items.filter((item => item.itreq?.length))
                case "send":
                        return items.filter((item) => {
                                return item.attrs.filter((attr) => {
                                        return (attr.name == "State" && attr.values[0].label == "ApprovedToBeSent")
                                }).length
                        })
        }
        return items

}


export default function ActionSelect() {
        const data = useContext(DataContext)
        const [items, setItems] = useContext(ItemsContext);
        const [results, setResults] = useContext(ResultContext);
        const [action, setAction] = useContext(ActionContext);

        useEffect(() => {
                const result = search(data, action)
                setItems(result);
                setResults(result);
        }, [action])

        return (
                <FormControl fullWidth>
                        <InputLabel id="action-select-label">Выберите действие</InputLabel>
                        <Select
                                labelId="action-select-label"
                                id="action-select"
                                value={action}
                                label="Выберите действие"
                                onChange={(event) => setAction(event.target.value)}>
                                <MenuItem value={""}>Всё</MenuItem>
                                <MenuItem value={"giveaway"}>Выдать</MenuItem>
                                <MenuItem value={'takeback'}>Сдать</MenuItem>
                                <MenuItem value={'send'}>Переслать</MenuItem>
                        </Select>
                </FormControl >
        )
}
