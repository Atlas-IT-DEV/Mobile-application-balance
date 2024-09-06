import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  TextInput,
} from "react-native";
import { SvgXml } from "react-native-svg";
import { arrowBack } from "../../images/images";

const EditProfileScreen = ({
  name = "Имя",
  surname = "Фамилия",
  phone_number = "+7 (800) 555 35-35",
  inn = "8888 888 888 88",
}) => {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView>
        <View style={styles.namePage}>
          <Text style={styles.namePageText}>Редактирование профиля</Text>
        </View>
        <TouchableOpacity style={styles.backButton}>
          <SvgXml xml={arrowBack} width={16} height={16} />
        </TouchableOpacity>

        <View style={styles.fields}>
          <View style={styles.divideLine} />
          <View style={styles.rowField}>
            <Text style={styles.attributeText}>Имя</Text>
            <TextInput style={styles.valueText} editable value={name}/>
          </View>
          <View style={styles.divideLine} />
          <View style={styles.rowField}>
            <Text style={styles.attributeText}>Фамилия</Text>
            <Text style={styles.valueText}>{surname}</Text>
          </View>
          <View style={styles.divideLine} />
          <View style={styles.rowField}>
            <Text style={styles.attributeText}>Телефон</Text>
            <Text style={styles.valueText}>{phone_number}</Text>
          </View>
          <View style={styles.divideLine} />
          <View style={styles.rowField}>
            <Text style={styles.attributeText}>Пароль</Text>
            <Text style={styles.valueText}>**********</Text>
          </View>
          <View style={styles.divideLine} />
          <View style={styles.rowField}>
            <Text style={styles.attributeText}>ИНН</Text>
            <Text style={styles.valueText}>{inn}</Text>
          </View>
          <View style={styles.divideLine} />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    width: "100%",
    height: "100%",
  },
  namePage: {
    // position: "relative",
    alignItems: "center",
    marginTop: 25,
  },
  namePageText: {
    color: "rgba(22, 3, 111, 1)",
    fontSize: 22,
    fontFamily: "IBMSemiBold",
  },
  backButton: {
    position: "absolute",
    top: 28,
    left: 15,
    padding: 5,
  },
  fields: {
    marginTop: 30,
    gap: 20,
    paddingHorizontal: 20,
  },
  divideLine: {
    width: "100%",
    height: 1,
    backgroundColor: "rgba(113, 113, 113, 1)",
  },

  rowField: {
    flexDirection: "row",
    alignItems: "center",
  },
  attributeText: {
    width: 100,
    color: "rgba(183, 183, 183, 1)",
    fontFamily: "IBMRegular",
    fontSize: 12,
  },
  valueText: {
    fontFamily: "IBMMedium",
    color: "rgba(52, 52, 52, 1)",
  },
});

export default EditProfileScreen;
