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
import { useNavigation } from "@react-navigation/native";

import { arrowBack } from "../../images/images";
import CheckBox from "react-native-check-box";
import { useState } from "react";

const RequestScreen = () => {
  const navigation = useNavigation();
  const [checked, setChecked] = useState(false);
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView>
        <View style={styles.namePage}>
          <Text style={styles.namePageText}>Заявка на регистрацию</Text>
        </View>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <SvgXml xml={arrowBack} width={16} height={16} />
        </TouchableOpacity>

        <Text style={styles.mainText}>
          Прежде чем начать процесс сбора средств на ваш благотворительный
          проект, мы просим вас заполнить эту краткую анкету. Ваши ответы
          помогут нам лучше понять цели вашего проекта и определить возможность
          его финансовой поддержки. Спасибо за ваше участие и стремление сделать
          мир лучше!
        </Text>

        <View style={styles.requestForm}>
          <View style={[styles.helpField, styles.component]}>
            <TextInput
              placeholder="Кому нужна помощь"
              placeholderTextColor={"rgba(183, 183, 183, 1)"}
            />
          </View>
          <View style={[styles.reasonField, styles.component]}>
            <TextInput
              placeholder="Причина обращения"
              placeholderTextColor={"rgba(183, 183, 183, 1)"}
            />
          </View>
          <View style={[styles.localityField, styles.component]}>
            <TextInput
              placeholder="Населенный пункт"
              placeholderTextColor={"rgba(183, 183, 183, 1)"}
            />
          </View>
          <View style={[styles.contactsField, styles.component]}>
            <TextInput
              placeholder="Контактный телефон"
              placeholderTextColor={"rgba(183, 183, 183, 1)"}
            />
          </View>
        </View>
        <TouchableOpacity style={styles.sendRequestButton}>
          <Text style={styles.sendRequestButtonText}>Отправить заявку</Text>
        </TouchableOpacity>

        <View style={styles.agreeView}>
          <CheckBox isChecked={checked} onClick={() => setChecked(!checked)} />
          <Text style={styles.agreeText}>
            Согласен с условиями Пользовательского соглашения и Политики
            обработки персональных данных
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    width: "100%",
    height: "100%",
    backgroundColor: "rgba(255,255,255,1)",
  },
  namePage: {
    alignItems: "center",
    marginTop: 25,
  },
  namePageText: {
    color: "rgba(22, 3, 111, 1)",
    fontSize: 18,
    fontFamily: "IBMSemiBold",
  },
  backButton: {
    position: "absolute",
    top: 25,
    left: 15,
    padding: 5,
  },
  mainText: {
    paddingHorizontal: 20,
    marginTop: 28,
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMRegular",
  },
  requestForm: {
    marginHorizontal: 20,
    marginTop: 30,
    gap: 15,
  },
  helpField: {
    justifyContent: "center",
    height: 40,
    paddingHorizontal: 20,
  },
  component: {
    backgroundColor: "rgba(255,255,255,1)",
    borderRadius: 10,
    shadowColor: "rgba(36, 27, 79, 0.2)",
    shadowOffset: {
      width: 0,
      height: 0,
    },
    shadowOpacity: 1,
    shadowRadius: 8,
  },
  reasonField: {
    height: 115,
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  localityField: {
    justifyContent: "center",
    height: 40,
    paddingHorizontal: 20,
  },
  contactsField: {
    justifyContent: "center",
    height: 40,
    paddingHorizontal: 20,
  },
  sendRequestButton: {
    alignItems: "center",
    marginTop: 15,
    backgroundColor: "rgba(48, 31, 129, 1)",
    height: 40,
    marginHorizontal: 20,
    justifyContent: "center",
    borderRadius: 10,
  },
  sendRequestButtonText: {
    fontFamily: "IBMSemiBold",
    color: "white",
  },
  agreeView: {
    flexDirection: "row",
    marginTop: 15,
    marginHorizontal: 20,
    gap: 8,
    alignItems: "center",
  },
  agreeText: {
    fontSize: 10,
    color: "rgba(183, 183, 183, 1)",
    fontFamily: "IBMMedium",
    paddingRight: 20,
  },
});

export default RequestScreen;
