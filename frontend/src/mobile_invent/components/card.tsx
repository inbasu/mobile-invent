import Grid from "@mui/material/Grid2";
import { Item, Values } from "../datatypes"
import ButtonGroup from "./buttonsGrp";
import { useContext } from "react";
import { ActionContext, ItemContext } from "../context";
import { Typography } from "@mui/material";


const hardwareFields = ["INV No", "Serial No", "Model", "State", "Location", "User", "Store"];
const ereqFields = ['Кто принял', 'Дата сдачи', "Кто выдал", 'Дата выдачи', "Пользователь"];



const AttrRow = ({ attr }: { attr: Values }) => {
        return (
                <>
                        <Grid size={4}>{attr.name}:</Grid>
                        <Grid size={8}>{attr.values[0] ? attr.values[0].label : ''}</Grid>
                </>)
}

export default function ItemCard() {
        const [item, setItem] = useContext(ItemContext);
        const [action, setAction] = useContext(ActionContext);


        return (
                <Grid container p={2}>
                        <Grid size={12}><h3>{item?.label}</h3></Grid>
                        <Grid container size={12} pb={3}>
                                <Grid size={12}><Typography variant='overline'>Оборудование</Typography></Grid>
                                {item?.attrs && item.attrs.map(attr => {
                                        if (hardwareFields.includes(attr.name) && attr.values) {
                                                return (<AttrRow attr={attr} />)
                                        }
                                })}
                        </Grid>
                        {item?.joined.length !== 0 &&
                                <Grid container size={12} pb={3}>
                                        <Grid size={12}><Typography variant='overline'>Карточка</Typography></Grid>
                                        {item?.joined && item.joined[0]?.attrs?.map(attr => {
                                                if (ereqFields.includes(attr.name)) {
                                                        return (<AttrRow attr={attr} />)

                                                }
                                        })}
                                </Grid>
                        }
                        {item?.itreq &&
                                <Grid container size={12} pb={3}>
                                        <Grid size={12}><Typography variant='overline'>Заявка</Typography></Grid>
                                        {item?.joined && item.joined[0]?.attrs?.map(attr => {
                                                if (ereqFields.includes(attr.name)) {
                                                        return (<AttrRow attr={attr} />)

                                                }
                                        })}
                                </Grid>
                        }

                        <Grid size={12}>
                                {action && <ButtonGroup />}
                        </Grid>
                </Grid>)
}
